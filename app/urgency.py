from typing import List, Dict, Tuple

from app.models import Pilot, Drone, Mission
from app.conflict_detector import ConflictDetector


class UrgencyCoordinator:
    """
    Handles urgent reassignment scenarios with minimal disruption.
    """

    def __init__(
        self,
        pilots: List[Pilot],
        drones: List[Drone],
        missions: List[Mission],
    ):
        self.pilots = pilots
        self.drones = drones
        self.missions = missions
        self.detector = ConflictDetector(pilots, drones, missions)

    # -------------------------
    # PUBLIC API
    # -------------------------

    def resolve_urgent_pilot_failure(
        self, mission_id: str
    ) -> Dict[str, str]:
        """
        Handles sudden pilot unavailability.
        Returns an explainable resolution.
        """
        mission = self._get_mission(mission_id)

        if not mission:
            return {"status": "error", "message": "Mission not found."}

        candidates = self._rank_pilot_candidates(mission)

        if not candidates:
            return {
                "status": "failed",
                "message": (
                    "URGENT FAILURE: No suitable standby pilots available.\n"
                    "Manual escalation required."
                ),
            }

        selected_pilot, rationale = candidates[0]

        # Apply reassignment
        mission.assigned_pilot_id = selected_pilot.id
        selected_pilot.current_assignment = mission.id
        selected_pilot.status = "Unavailable"

        return {
            "status": "success",
            "message": (
                f"URGENT REASSIGNMENT COMPLETE\n"
                f"Mission: {mission.name}\n"
                f"New Pilot: {selected_pilot.name}\n"
                f"Rationale: {rationale}"
            ),
        }

    # -------------------------
    # RANKING LOGIC
    # -------------------------

    def _rank_pilot_candidates(
        self, mission: Mission
    ) -> List[Tuple[Pilot, str]]:
        """
        Rank pilots by lowest operational disruption.
        """
        ranked: List[Tuple[Pilot, str]] = []

        for pilot in self.pilots:
            conflicts = self.detector.check_assignment(
                pilot=pilot,
                drone=self._dummy_drone(),
                mission=mission,
            )

            if conflicts["blockers"]:
                continue

            score = 0
            reasons = []

            if pilot.current_location == mission.location:
                score += 3
                reasons.append("same location")

            skill_overlap = len(
                set(pilot.drone_experience).intersection(
                    mission.required_skills
                )
            )
            if skill_overlap:
                score += skill_overlap
                reasons.append("skill match")

            cert_overlap = len(
                set(pilot.certifications).intersection(
                    mission.required_certifications
                )
            )
            if cert_overlap:
                score += cert_overlap
                reasons.append("certified")

            ranked.append(
                (
                    pilot,
                    f"Selected due to {' + '.join(reasons)}"
                    if reasons
                    else "Meets minimum requirements",
                )
            )

        ranked.sort(key=lambda x: x[0].name)  # deterministic
        ranked.sort(key=lambda x: len(x[1]), reverse=True)

        return ranked

    # -------------------------
    # HELPERS
    # -------------------------

    def _get_mission(self, mission_id: str) -> Mission | None:
        return next(
            (m for m in self.missions if m.id == mission_id), None
        )

    @staticmethod
    def _dummy_drone() -> Drone:
        """
        Used for pilot-only conflict checks.
        """
        return Drone(
            id="DUMMY",
            model="N/A",
            capabilities=[],
            current_location="N/A",
            status="Available",
        )
