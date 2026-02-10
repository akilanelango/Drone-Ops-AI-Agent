from typing import List
from datetime import date

from app.models import Pilot, Drone, Mission
from app.data_loader import load_pilots, load_drones, load_missions


class OpsAgent:
    """
    Drone Operations Coordinator AI Agent
    """

    def __init__(
        self,
        pilot_csv: str,
        drone_csv: str,
        mission_csv: str,
    ):
        self.pilots: List[Pilot] = load_pilots(pilot_csv)
        self.drones: List[Drone] = load_drones(drone_csv)
        self.missions: List[Mission] = load_missions(mission_csv)

    # -------------------------
    # ENTRYPOINT
    # -------------------------

    def handle(self, user_input: str) -> str:
        user_input = user_input.lower()

        if "available pilot" in user_input:
            return self._handle_available_pilots()

        if "available drone" in user_input:
            return self._handle_available_drones()

        if "assign" in user_input:
            return self._handle_assignment_request()

        if "urgent" in user_input or "emergency" in user_input:
            return self._handle_urgent_reassignment()

        return (
            "I’m not fully sure what you want yet.\n\n"
            "You can ask things like:\n"
            "- Which pilots are available?\n"
            "- Which drones are available?\n"
            "- Assign resources to a mission\n"
            "- Handle an urgent reassignment"
        )

    # -------------------------
    # HANDLERS
    # -------------------------

    def _handle_available_pilots(self) -> str:
        available = [p for p in self.pilots if p.is_available()]

        if not available:
            return "No pilots are currently available."

        response = "Available pilots:\n"
        for p in available:
            response += f"- {p.name} ({p.skill_level}, {p.current_location})\n"

        return response

    def _handle_available_drones(self) -> str:
        available = [d for d in self.drones if d.is_operational()]

        if not available:
            return "No drones are currently available."

        response = "Available drones:\n"
        for d in available:
            response += f"- {d.model} ({d.current_location})\n"

        return response

    def _handle_assignment_request(self) -> str:
        """
        Naive first-pass assignment logic.
        We improve this later with conflict detection.
        """
        unassigned_missions = [
            m for m in self.missions if m.assigned_pilot_id is None
        ]

        if not unassigned_missions:
            return "All missions are currently assigned."

        mission = unassigned_missions[0]

        pilot = next((p for p in self.pilots if p.is_available()), None)
        drone = next((d for d in self.drones if d.is_operational()), None)

        if not pilot or not drone:
            return (
                "Unable to assign mission due to lack of available pilots or drones."
            )

        # Assign
        pilot.current_assignment = mission.id
        pilot.status = "Unavailable"

        drone.current_assignment = mission.id
        drone.status = "Deployed"

        mission.assigned_pilot_id = pilot.id
        mission.assigned_drone_id = drone.id

        return (
            f"Mission '{mission.name}' assigned successfully.\n"
            f"Pilot: {pilot.name}\n"
            f"Drone: {drone.model}\n"
            f"Location: {mission.location}"
        )

    def _handle_urgent_reassignment(self) -> str:
        """
        Emergency logic: find least disruptive reassignment.
        """
        active_missions = [
            m for m in self.missions if m.assigned_pilot_id is not None
        ]

        if not active_missions:
            return "No active missions to reassign."

        mission = active_missions[0]

        available_pilot = next(
            (p for p in self.pilots if p.is_available()), None
        )

        if not available_pilot:
            return (
                "Urgent reassignment failed: no standby pilots available.\n"
                "Manual intervention required."
            )

        old_pilot_id = mission.assigned_pilot_id
        mission.assigned_pilot_id = available_pilot.id

        available_pilot.current_assignment = mission.id
        available_pilot.status = "Unavailable"

        return (
            f"URGENT REASSIGNMENT COMPLETE\n"
            f"Mission: {mission.name}\n"
            f"Previous pilot: {old_pilot_id}\n"
            f"New pilot: {available_pilot.name}\n"
            f"Impact: Minimal disruption"
        )
