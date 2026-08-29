from pydantic import BaseModel, Field
from typing import List, Optional


class CandidateInput(BaseModel):

    Resume_ID: str = Field(
        default="NEW_CANDIDATE"
    )

    Name: str

    Skills: str

    Experience_Years: float = Field(
        ge=0
    )

    Education: str

    Certifications: str = ""

    Job_Role: str

    Salary_Expectation: float = Field(
        ge=0
    )

    Projects_Count: int = Field(
        ge=0
    )

    AI_Score: float = Field(
        ge=0,
        le=100
    )


class PredictionResponse(BaseModel):

    Resume_ID: str

    Name: str

    Job_Role: str

    Hire_Probability: float

    Recommendation: str


class JobFitResponse(BaseModel):

    Resume_ID: str

    Job_Role: str

    Job_Fit_Score: float

    Matched_Skills: List[str]

    Missing_Skills: List[str]


class CandidateReportResponse(BaseModel):

    Resume_ID: str

    Name: str

    Job_Role: str

    Hire_Probability: float

    Job_Fit_Score: float

    Candidate_Strength_Score: float

    Recruitment_Score: float

    Recommendation: str

    Matched_Skills: List[str]

    Missing_Skills: List[str]

    Positive_Model_Factors: List[str]

    Negative_Model_Factors: List[str]


class CandidateReportResponse(BaseModel):

    Resume_ID: str

    Name: str

    Job_Role: str

    Hire_Probability: float

    Job_Fit_Score: float

    Candidate_Strength_Score: float

    Recruitment_Score: float

    Recommendation: str

    Matched_Skills: List[str]

    Missing_Skills: List[str]

    Positive_Model_Factors: List[str]

    Negative_Model_Factors: List[str]

    SHAP_Features: list


class CandidateListResponse(BaseModel):

    candidates: list

    total: int


class CandidateStatisticsResponse(BaseModel):

    total_candidates: int

    average_hire_probability: float

    average_job_fit: float

    average_recruitment_score: float

    recommendations: dict

    job_roles: dict
