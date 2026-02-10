import pandas as pd
from typing import List
from datetime import datetime

from app.models import Pilot, Drone, Mission


# -------------------------
# HELPERS
# -------------------------

def _parse_list(value) -> List[str]:
    if pd.isna(value) or not value:
        return []
    return [v.strip() for v in str(value).split(",")]


def _parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


# -------------------------
# LOADERS
# -------------------------

def load_pilots(csv_path: str) -> List[Pilot]:
    df = pd.read_csv(csv_path)
    pilots: List[Pilot] = []

    for _, row in df.iterrows():
        pilot = Pilot(
            id=str(row["pilot_id"]),
            name=row["name"],
            skill_level=",".join(_parse_list(row["skills"])),
            certifications=_parse_list(row["certifications"]),
            drone_experience=_parse_list(row["skills"]),
            current_location=row["location"],
            status=row["status"],
            current_assignment=(
                str(row["current_assignment"])
                if not pd.isna(row["current_assignment"])
                else None
            ),
        )
        pilots.append(pilot)

    return pilots


def load_drones(csv_path: str) -> List[Drone]:
    df = pd.read_csv(csv_path)
    drones: List[Drone] = []

    for _, row in df.iterrows():
        drone = Drone(
            id=str(row["drone_id"]),
            model=row["model"],
            capabilities=_parse_list(row["capabilities"]),
            current_location=row["location"],
            status=row["status"],
            current_assignment=(
                str(row["current_assignment"])
                if not pd.isna(row["current_assignment"])
                else None
            ),
        )
        drones.append(drone)

    return drones


def load_missions(csv_path: str) -> List[Mission]:
    df = pd.read_csv(csv_path)
    missions: List[Mission] = []

    for _, row in df.iterrows():
        mission = Mission(
            id=str(row["project_id"]),
            name=row["client"],
            required_skills=_parse_list(row["required_skills"]),
            required_certifications=_parse_list(row["required_certs"]),
            required_drone_capabilities=[],
            location=row["location"],
            start_date=_parse_date(row["start_date"]),
            end_date=_parse_date(row["end_date"]),
            assigned_pilot_id=None,
            assigned_drone_id=None,
        )
        missions.append(mission)

    return missions
