from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field


# -------------------------
# CORE DOMAIN MODELS
# -------------------------

class Pilot(BaseModel):
    id: str
    name: str
    skill_level: str
    certifications: List[str]
    drone_experience: List[str]
    current_location: str

    status: str = Field(
        default="Available",
        description="Available | On Leave | Unavailable"
    )

    current_assignment: Optional[str] = None

    def is_available(self) -> bool:
        return self.status == "Available" and self.current_assignment is None


class Drone(BaseModel):
    id: str
    model: str
    capabilities: List[str]
    current_location: str

    status: str = Field(
        default="Available",
        description="Available | In Maintenance | Deployed"
    )

    current_assignment: Optional[str] = None

    def is_operational(self) -> bool:
        return self.status == "Available" and self.current_assignment is None


class Mission(BaseModel):
    id: str
    name: str
    required_skills: List[str]
    required_certifications: List[str]
    required_drone_capabilities: List[str]

    location: str
    start_date: date
    end_date: date

    assigned_pilot_id: Optional[str] = None
    assigned_drone_id: Optional[str] = None

    def is_active_on(self, check_date: date) -> bool:
        return self.start_date <= check_date <= self.end_date


class Assignment(BaseModel):
    mission_id: str
    pilot_id: str
    drone_id: str

    start_date: date
    end_date: date

    location: str
