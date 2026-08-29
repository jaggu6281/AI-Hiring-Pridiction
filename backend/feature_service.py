import pandas as pd


# ============================================================
# FEATURE SERVICE
# ============================================================

def parse_list(value):
    """
    Convert comma/semicolon/pipe separated text
    into a cleaned list.
    """

    if value is None:
        return []

    text = str(value).strip()

    if not text:
        return []

    text = text.replace(";", ",")
    text = text.replace("|", ",")

    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


def build_candidate_features(candidate):
    """
    Convert API candidate data into exactly the
    feature columns expected by the trained model.
    """

    skills = parse_list(
        candidate.Skills
    )

    certifications = parse_list(
        candidate.Certifications
    )

    experience = float(
        candidate.Experience_Years
    )

    projects = int(
        candidate.Projects_Count
    )

    skill_count = len(
        skills
    )

    certification_count = len(
        certifications
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # This must match the feature engineering used during
    # model training.
    # --------------------------------------------------------

    project_experience_index = (
        projects * max(
            experience,
            1
        )
    )

    features = {

        "Experience (Years)": [
            experience
        ],

        "Salary Expectation ($)": [
            float(
                candidate.Salary_Expectation
            )
        ],

        "Projects Count": [
            projects
        ],

        "Skill_Count": [
            skill_count
        ],

        "Certification_Count": [
            certification_count
        ],

        "Project_Experience_Index": [
            project_experience_index
        ],

        "Education": [
            candidate.Education
        ],

        "Job Role": [
            candidate.Job_Role
        ]
    }

    return pd.DataFrame(
        features
    )
