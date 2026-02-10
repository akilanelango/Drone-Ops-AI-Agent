from typing import List, Dict
from datetime import date

from app.models import Pilot, Drone, Mission


class ConflictDetector:
    """
    Detects conflicts and warnings when assigning pilots and drones to missions.
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

    # -------------------------
    # PUBLIC API
    # -------------------------

    def check_assignment(
        self,
        pilot: Pilot,
        drone: Drone,
        mission: Mission,
    ) -> Dict[str, List[str]]:
        """
        Returns a dict with:
        - blockers: hard-stop conflicts
        - warnings: non-blocking issues
        """
        blockers: List[str] = []
        warnings: List[str] = []

        blockers.extend(self._pilot_availability_conflicts(pilot, mission))
        blockers.extend(self._pilot_skill_conflicts(pilot, mission))
        blockers.extend(self._pilot_certification_conflicts(pilot, mission))

        blockers.extend(self._drone_status_conflicts(drone))
        blockers.extend(self._drone_capability_conflicts(drone, mission))

        warnings.extend(self._location_mismatch_warnings(pilot, drone, mission))

        return {
            "blockers": blockers,
            "warnings": warnings,
        }

    # -------------------------
    # PILOT CONFLICTS
    # -------------------------

    def _pilot_availability_conflicts(
        self, pilot: Pilot, mission: Mission
    ) -> List[str]:
        conflicts = []

        if not pilot.is_available():
            conflicts.append(
                f"Pilot {pilot.name} is not available (status: {pilot.status})."
            )

        # Overlapping mission dates
        for m in self.missions:
            if m.assigned_pilot_id == pilot.id:
                if self._dates_overlap(m, mission):
                    conflicts.append(
                        f"Pilot {pilot.name} is already assigned to mission "
                        f"{m.name} during overlapping dates."
                    )

        return conflicts

    def _pilot_skill_conflicts(
        self, pilot: Pilot, mission: Mission
    ) -> List[str]:
        missing_skills = [
            skill
            for skill in mission.required_skills
            if skill not in pilot.drone_experience
            and skill != pilot.skill_level
        ]

        if missing_skills:
            return [
                f"Pilot {pilot.name} lacks required skills: "
                f"{', '.join(missing_skills)}."
            ]

        return []

    def _pilot_certification_conflicts(
        self, pilot: Pilot, mission: Mission
    ) -> List[str]:
        missing_certs = [
            cert
            for cert in mission.required_certifications
            if cert not in pilot.certifications
        ]

        if missing_certs:
            return [
                f"Pilot {pilot.name} lacks required certifications: "
                f"{', '.join(missing_certs)}."
            ]

        return []

    # -------------------------
    # DRONE CONFLICTS
    # -------------------------

    def _drone_status_conflicts(self, drone: Drone) -> List[str]:
        if drone.status != "Available":
            return [
                f"Drone {drone.model} is not available "
                f"(status: {drone.status})."
            ]
        return []

    def _drone_capability_conflicts(
        self, drone: Drone, mission: Mission
    ) -> List[str]:
        missing_caps = [
            cap
            for cap in mission.required_drone_capabilities
            if cap not in drone.capabilities
        ]

        if missing_caps:
            return [
                f"Drone {drone.model} lacks required capabilities: "
                f"{', '.join(missing_caps)}."
            ]

        return []

    # -------------------------
    # WARNINGS (NON-BLOCKING)
    # -------------------------

    def _location_mismatch_warnings(
        self, pilot: Pilot, drone: Drone, mission: Mission
    ) -> List[str]:
        warnings = []

        if pilot.current_location != mission.location:
            warnings.append(
                f"Pilot {pilot.name} is currently in {pilot.current_location}, "
                f"mission location is {mission.location}."
            )

        if drone.current_location != mission.location:
            warnings.append(
                f"Drone {drone.model} is currently in {drone.current_location}, "
                f"mission location is {mission.location}."
            )

        return warnings

    # -------------------------
    # UTILITIES
    # -------------------------

    @staticmethod
    def _dates_overlap(m1: Mission, m2: Mission) -> bool:
        return not (m1.end_date < m2.start_date or m2.end_date < m1.start_date)
