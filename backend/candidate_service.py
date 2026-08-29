from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "enhanced_candidate_ranking.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

if not DATA_PATH.exists():

    raise FileNotFoundError(
        f"Candidate ranking file not found: {DATA_PATH}"
    )


candidates_df = pd.read_csv(
    DATA_PATH
)


# ============================================================
# CLEAN NaN VALUES
# ============================================================

candidates_df = (
    candidates_df
    .replace(
        {float("nan"): None}
    )
)


# ============================================================
# GET ALL CANDIDATES
# ============================================================

def get_all_candidates():

    return candidates_df.copy()


# ============================================================
# GET CANDIDATE BY RESUME ID
# ============================================================

def get_candidate(
    resume_id
):

    matches = candidates_df[
        candidates_df["Resume_ID"].astype(str)
        == str(resume_id)
    ]

    if matches.empty:

        return None

    return matches.iloc[0].to_dict()


# ============================================================
# GET TOP CANDIDATES
# ============================================================

def get_top_candidates(
    limit=10
):

    limit = max(
        1,
        min(
            int(limit),
            100
        )
    )

    return (
        candidates_df
        .sort_values(
            "Recruitment_Score",
            ascending=False
        )
        .head(limit)
        .to_dict(
            orient="records"
        )
    )


# ============================================================
# FILTER CANDIDATES
# ============================================================

def filter_candidates(
    job_role=None,
    recommendation=None,
    min_score=None,
    search=None
):

    df = candidates_df.copy()

    # --------------------------------------------------------
    # Job role
    # --------------------------------------------------------

    if job_role:

        df = df[
            df["Job Role"]
            .astype(str)
            .str.lower()
            ==
            str(job_role).lower()
        ]

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if recommendation:

        df = df[
            df["Recommendation"]
            .astype(str)
            .str.lower()
            ==
            str(recommendation).lower()
        ]

    # --------------------------------------------------------
    # Minimum recruitment score
    # --------------------------------------------------------

    if min_score is not None:

        df = df[
            df["Recruitment_Score"]
            >= float(min_score)
        ]

    # --------------------------------------------------------
    # Search candidate
    # --------------------------------------------------------

    if search:

        search_text = (
            str(search)
            .lower()
        )

        mask = (

            df["Name"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )

            |

            df["Resume_ID"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        )

        df = df[mask]

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = (
        df
        .sort_values(
            "Recruitment_Score",
            ascending=False
        )
    )

    return df.to_dict(
        orient="records"
    )


# ============================================================
# DATASET STATISTICS
# ============================================================

def get_candidate_statistics():

    total = len(
        candidates_df
    )

    recommendations = (
        candidates_df[
            "Recommendation"
        ]
        .value_counts()
        .to_dict()
    )

    roles = (
        candidates_df[
            "Job Role"
        ]
        .value_counts()
        .to_dict()
    )

    average_hire_probability = (
        candidates_df[
            "Hire_Probability"
        ]
        .mean()
    )

    average_job_fit = (
        candidates_df[
            "Job_Fit_Score"
        ]
        .mean()
    )

    average_recruitment_score = (
        candidates_df[
            "Recruitment_Score"
        ].mean()
    )

    return {

        "total_candidates":
            int(total),

        "average_hire_probability":
            round(
                float(
                    average_hire_probability
                ),
                2
            ),

        "average_job_fit":
            round(
                float(
                    average_job_fit
                ),
                2
            ),

        "average_recruitment_score":
            round(
                float(
                    average_recruitment_score
                ),
                2
            ),

        "recommendations":
            recommendations,

        "job_roles":
            roles
    }
