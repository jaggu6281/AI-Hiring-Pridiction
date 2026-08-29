from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap

try:
    from .model_service import (
        model,
        get_recommendation
    )

    from .skill_service import (
        calculate_job_fit
    )
except ImportError:
    from model_service import (
        model,
        get_recommendation
    )

    from skill_service import (
        calculate_job_fit
    )


# ============================================================
# PATHS
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

MODEL_DIR = (
    BASE_DIR /
    "models"
)


STRENGTH_SCALER_PATH = (
    MODEL_DIR /
    "candidate_strength_scaler.pkl"
)


# ============================================================
# LOAD STRENGTH SCALER
# ============================================================

if not STRENGTH_SCALER_PATH.exists():

    raise FileNotFoundError(
        "Candidate strength scaler not found: "
        f"{STRENGTH_SCALER_PATH}"
    )


strength_scaler = joblib.load(
    STRENGTH_SCALER_PATH
)


# ============================================================
# GET MODEL COMPONENTS
# ============================================================

preprocessor = (
    model.named_steps["preprocessor"]
)

classifier = (
    model.named_steps["classifier"]
)


# ============================================================
# FEATURE NAMES
# ============================================================

feature_names = (
    preprocessor
    .get_feature_names_out()
)


# ============================================================
# SHAP EXPLAINER
# ============================================================

explainer = shap.TreeExplainer(
    classifier
)


# ============================================================
# CANDIDATE STRENGTH
# ============================================================

def calculate_candidate_strength(
    experience,
    projects,
    skill_count,
    certification_count
):

    values = pd.DataFrame({

        "Experience (Years)": [
            experience
        ],

        "Projects Count": [
            projects
        ],

        "Skill_Count": [
            skill_count
        ],

        "Certification_Count": [
            certification_count
        ]
    })

    scaled = strength_scaler.transform(
        values
    )

    scaled_df = pd.DataFrame(
        scaled,
        columns=values.columns
    )

    score = (

        scaled_df[
            "Experience (Years)"
        ].iloc[0] * 0.35

        +

        scaled_df[
            "Projects Count"
        ].iloc[0] * 0.25

        +

        scaled_df[
            "Skill_Count"
        ].iloc[0] * 0.25

        +

        scaled_df[
            "Certification_Count"
        ].iloc[0] * 0.15

    ) * 100

    # Keep score within display range
    score = max(
        0,
        min(
            100,
            score
        )
    )

    return float(score)


# ============================================================
# SHAP EXPLANATION
# ============================================================

def get_shap_explanation(
    features
):

    transformed = (
        preprocessor.transform(
            features
        )
    )

    raw_values = (
        explainer.shap_values(
            transformed
        )
    )

    shap_array = np.asarray(
        raw_values
    )

    # SHAP version compatibility
    if shap_array.ndim == 3:

        shap_values = (
            shap_array[0, :, 1]
        )

    elif shap_array.ndim == 2:

        shap_values = (
            shap_array[0]
        )

    else:

        shap_values = shap_array

    if len(shap_values) != len(
        feature_names
    ):

        raise ValueError(
            "SHAP feature count does not "
            "match model feature count."
        )

    explanation = pd.DataFrame({

        "Feature":
            feature_names,

        "SHAP_Value":
            shap_values

    })

    explanation["Impact"] = (
        explanation["SHAP_Value"]
        .abs()
    )

    explanation = (
        explanation
        .sort_values(
            "Impact",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    positive = (
        explanation[
            explanation["SHAP_Value"] > 0
        ]
        .head(5)
    )

    negative = (
        explanation[
            explanation["SHAP_Value"] < 0
        ]
        .sort_values(
            "SHAP_Value"
        )
        .head(5)
    )

    return {

        "top_features":
            explanation.head(10).to_dict(
                orient="records"
            ),

        "positive_factors":
            positive["Feature"].tolist(),

        "negative_factors":
            negative["Feature"].tolist()
    }


# ============================================================
# COMPLETE CANDIDATE REPORT
# ============================================================

def generate_candidate_report(
    candidate,
    features,
    prediction,
    probability
):

    # --------------------------------------------------------
    # Parse skills
    # --------------------------------------------------------

    skills_text = (
        candidate.Skills
    )

    skill_parts = (
        str(skills_text)
        .replace(";", ",")
        .replace("|", ",")
        .split(",")
    )

    skills = [
        skill.strip()
        for skill in skill_parts
        if skill.strip()
    ]

    certifications = (
        str(
            candidate.Certifications
        )
        .replace(";", ",")
        .replace("|", ",")
        .split(",")
    )

    certifications = [
        cert.strip()
        for cert in certifications
        if cert.strip()
    ]

    skill_count = len(
        skills
    )

    certification_count = len(
        certifications
    )

    # --------------------------------------------------------
    # Job fit
    # --------------------------------------------------------

    job_fit = calculate_job_fit(
        candidate.Skills,
        candidate.Job_Role
    )

    # --------------------------------------------------------
    # Candidate strength
    # --------------------------------------------------------

    strength_score = (
        calculate_candidate_strength(
            candidate.Experience_Years,
            candidate.Projects_Count,
            skill_count,
            certification_count
        )
    )

    # --------------------------------------------------------
    # Recruitment score
    # --------------------------------------------------------

    recruitment_score = (

        probability * 0.60

        +

        job_fit["job_fit_score"] * 0.25

        +

        strength_score * 0.15

    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    recommendation = (
        get_recommendation(
            probability
        )
    )

    # --------------------------------------------------------
    # SHAP
    # --------------------------------------------------------

    shap_result = get_shap_explanation(
        features
    )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {

        "Resume_ID":
            candidate.Resume_ID,

        "Name":
            candidate.Name,

        "Job_Role":
            candidate.Job_Role,

        "Hire_Probability":
            round(
                float(probability),
                2
            ),

        "Job_Fit_Score":
            round(
                float(
                    job_fit[
                        "job_fit_score"
                    ]
                ),
                2
            ),

        "Candidate_Strength_Score":
            round(
                strength_score,
                2
            ),

        "Recruitment_Score":
            round(
                recruitment_score,
                2
            ),

        "Recommendation":
            recommendation,

        "Matched_Skills":
            job_fit[
                "matched_skills"
            ],

        "Missing_Skills":
            job_fit[
                "missing_skills"
            ],

        "Positive_Model_Factors":
            shap_result[
                "positive_factors"
            ],

        "Negative_Model_Factors":
            shap_result[
                "negative_factors"
            ],

        "SHAP_Features":
            shap_result[
                "top_features"
            ]
    }
