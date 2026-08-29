from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from .feature_service import (
        build_candidate_features
    )

    from .schemas import (
        CandidateInput,
        CandidateStatisticsResponse,
        PredictionResponse,
        JobFitResponse,
        CandidateReportResponse
    )

    from .model_service import (
        predict,
        get_recommendation
    )

    from .skill_service import (
        calculate_job_fit
    )
    from .report_service import (
        generate_candidate_report
    )
    from .candidate_service import (
        get_all_candidates,
        get_candidate,
        get_top_candidates,
        filter_candidates,
        get_candidate_statistics
    )
except ImportError:
    from feature_service import (
        build_candidate_features
    )

    from schemas import (
        CandidateInput,
        CandidateStatisticsResponse,
        PredictionResponse,
        JobFitResponse,
        CandidateReportResponse
    )

    from model_service import (
        predict,
        get_recommendation
    )

    from skill_service import (
        calculate_job_fit
    )
    from report_service import (
        generate_candidate_report
    )
    from candidate_service import (
        get_all_candidates,
        get_candidate,
        get_top_candidates,
        filter_candidates,
        get_candidate_statistics
    )

# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI Hiring Prediction API",
    description=(
        "AI-assisted candidate prediction, "
        "ranking and job-fit analysis API."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def root():

    return {
        "message": "AI Hiring Prediction API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# Prediction API
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_candidate(
    candidate: CandidateInput
):

    try:

        features = build_candidate_features(
            candidate
        )

        prediction, probability = predict(
            features
        )

        recommendation = (
            get_recommendation(
                probability
            )
        )

        return {
            "Resume_ID":
                candidate.Resume_ID,

            "Name":
                candidate.Name,

            "Job_Role":
                candidate.Job_Role,

            "Hire_Probability":
                round(
                    probability,
                    2
                ),

            "Recommendation":
                recommendation
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Job Fit API
# ============================================================

@app.post(
    "/job-fit",
    response_model=JobFitResponse
)
def job_fit(
    candidate: CandidateInput
):

    result = calculate_job_fit(
        candidate.Skills,
        candidate.Job_Role
    )

    return {

        "Resume_ID":
            candidate.Resume_ID,

        "Job_Role":
            candidate.Job_Role,

        "Job_Fit_Score":
            result["job_fit_score"],

        "Matched_Skills":
            result["matched_skills"],

        "Missing_Skills":
            result["missing_skills"]
    }


@app.post("/debug/features")
def debug_features(
    candidate: CandidateInput
):

    features = build_candidate_features(
        candidate
    )

    return {
        "columns": features.columns.tolist(),
        "values": features.iloc[0].to_dict()
    }
# ============================================================
# COMPLETE AI CANDIDATE REPORT
# ============================================================


@app.post(
    "/candidate-report",
    response_model=CandidateReportResponse
)
def candidate_report(
    candidate: CandidateInput
):

    try:

        # ----------------------------------------------------
        # Build exact model features
        # ----------------------------------------------------

        features = (
            build_candidate_features(
                candidate
            )
        )

        # ----------------------------------------------------
        # Model prediction
        # ----------------------------------------------------

        prediction, probability = (
            predict(
                features
            )
        )

        # ----------------------------------------------------
        # Generate complete report
        # ----------------------------------------------------

        report = (
            generate_candidate_report(
                candidate,
                features,
                prediction,
                probability
            )
        )

        return report

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ============================================================
# ALL CANDIDATES
# ============================================================


@app.get("/candidates")
def candidates():

    data = get_all_candidates()

    return {
        "total": len(data),
        "candidates": data.to_dict(
            orient="records"
        )
    }
# ============================================================
# TOP CANDIDATES
# ============================================================


@app.get("/candidates/top")
def top_candidates(
    limit: int = 10
):

    return {
        "limit": limit,
        "candidates":
            get_top_candidates(
                limit
            )
    }
# ============================================================
# FILTER CANDIDATES
# ============================================================


@app.get("/candidates/search")
def search_candidates(

    job_role: str | None = None,

    recommendation: str | None = None,

    min_score: float | None = None,

    search: str | None = None

):

    results = filter_candidates(

        job_role=job_role,

        recommendation=recommendation,

        min_score=min_score,

        search=search
    )

    return {

        "total":
            len(results),

        "candidates":
            results
    }
# ============================================================
# CANDIDATE STATISTICS
# ============================================================


@app.get(
    "/candidates/stats",
    response_model=CandidateStatisticsResponse
)
def candidate_statistics():

    return (
        get_candidate_statistics()
    )


@app.get(
    "/candidates/{resume_id}"
)
def candidate_by_id(
    resume_id: str
):

    candidate = get_candidate(
        resume_id
    )

    if candidate is None:

        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate
