from pathlib import Path
import pickle
import pandas as pd


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SKILL_PROFILE_PATH = (
    BASE_DIR
    / "models"
    / "role_required_skills.pkl"
)


# ------------------------------------------------------------
# Load role skill profiles
# ------------------------------------------------------------

if not SKILL_PROFILE_PATH.exists():

    raise FileNotFoundError(
        f"Skill profile file not found: "
        f"{SKILL_PROFILE_PATH}"
    )


with open(
    SKILL_PROFILE_PATH,
    "rb"
) as file:

    role_required_skills = pickle.load(
        file
    )


# ------------------------------------------------------------
# Parse skills
# ------------------------------------------------------------

def parse_skills(value):

    if value is None:
        return set()

    text = str(value).strip().lower()

    if not text:
        return set()

    text = text.replace(";", ",")
    text = text.replace("|", ",")
    text = text.replace("/", ",")

    return {
        skill.strip()
        for skill in text.split(",")
        if skill.strip()
    }


# ------------------------------------------------------------
# Calculate job fit
# ------------------------------------------------------------

def calculate_job_fit(
    skills,
    job_role
):

    candidate_skills = parse_skills(
        skills
    )

    required_skills = role_required_skills.get(
        job_role,
        set()
    )

    if not required_skills:

        return {
            "job_fit_score": 0.0,
            "matched_skills": [],
            "missing_skills": []
        }

    matched = (
        candidate_skills
        & required_skills
    )

    missing = (
        required_skills
        - candidate_skills
    )

    score = (
        len(matched)
        / len(required_skills)
    ) * 100

    return {
        "job_fit_score": round(
            score,
            2
        ),
        "matched_skills": sorted(
            matched
        ),
        "missing_skills": sorted(
            missing
        )
    }
