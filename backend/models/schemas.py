from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from backend.services.sanitizer import (
    sanitize_text,
    sanitize_email,
    sanitize_identifier,
    sanitize_skills_list
)

class ResumeUploadResponse(BaseModel):
    skills: List[str] = []
    education: List[Union[Dict[str, Any], str]] = []
    experience: Union[List[Dict[str, Any]], Dict[str, Any]] = []
    certifications: List[str] = []
    raw_text: str = ""
    confidence_score: float = 1.0
    is_scanned_or_low_text: bool = False
    warning_message: Optional[str] = None

class SkillNormalizeRequest(BaseModel):
    skills: List[str]

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        return sanitize_skills_list(v)

class SkillNormalizeResponse(BaseModel):
    normalized_skills: List[str]

class RoleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    essential_skills: List[str] = []
    optional_skills: List[str] = []
    avg_salary: Optional[Union[str, float]] = None
    experience_range: Optional[str] = None

class GapAnalysisRequest(BaseModel):
    user_skills: List[str] = Field(default=[], alias="userSkills")
    target_role_id: str = Field(..., alias="targetRoleId")

    model_config = {
        "populate_by_name": True
    }

    @field_validator("target_role_id")
    @classmethod
    def validate_role_id(cls, v: str) -> str:
        return sanitize_identifier(v, field_name="Target Role ID")

    @field_validator("user_skills")
    @classmethod
    def validate_user_skills(cls, v: List[str]) -> List[str]:
        return sanitize_skills_list(v)

class GapAnalysisResponse(BaseModel):
    fit_score: float
    essential_coverage: float
    optional_coverage: float
    missing_essential: List[str]
    missing_optional: List[str]
    matched_skills: List[str]
    surplus_skills: List[str]
    total_required: int = 0
    matched_count: int = 0
    why_this_role: Optional[str] = None
    predicted_salary: Optional[str] = None
    skill_velocities: Optional[List[Dict[str, Any]]] = None
    confidence_level: str = "High"
    is_exploratory_mode: bool = False
    disclaimer: Optional[str] = "Estimated market compensation reflects median hiring data for candidates clearing technical rounds and is not a guaranteed job offer."

class RecommendationRequest(BaseModel):
    user_skills: List[str] = Field(default=[], alias="userSkills")
    user_education: Optional[Union[List[str], List[Dict[str, Any]]]] = Field(default=[], alias="education")
    user_experience: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(default={}, alias="experience")
    raw_text: Optional[str] = ""

    model_config = {
        "populate_by_name": True
    }

    @field_validator("user_skills")
    @classmethod
    def validate_skills(cls, v: List[str]) -> List[str]:
        return sanitize_skills_list(v)

class RecommendationResponse(BaseModel):
    role_id: str
    role_title: str
    score: float
    explanation: str

class RoadmapRequest(BaseModel):
    missing_skills: List[str] = Field(default=[], alias="missingSkills")
    preferences: Optional[Dict[str, Any]] = None

    model_config = {
        "populate_by_name": True
    }

    @field_validator("missing_skills")
    @classmethod
    def validate_missing(cls, v: List[str]) -> List[str]:
        return sanitize_skills_list(v)

class RoadmapEntry(BaseModel):
    week: int
    skill: str
    course: str
    platform: str
    url: Optional[str] = None
    project: str
    duration: str
    is_free: bool = True
    difficulty: str = "Beginner"
    initiative: Optional[str] = None
    is_govt_initiative: bool = False

class RoadmapResponse(BaseModel):
    entries: List[RoadmapEntry]

class UserProfile(BaseModel):
    skills: List[str] = []
    education: List[Union[Dict[str, Any], str]] = []
    experience: Union[List[Dict[str, Any]], Dict[str, Any]] = []
    certifications: List[str] = []

# ==============================================================================
# AUTH & INSTITUTION SCHEMAS
# ==============================================================================
class UserRegisterRequest(BaseModel):
    email: str
    password: str
    user_name: str
    role: str = "candidate"  # "candidate" or "institution_admin"
    institution_name: Optional[str] = "All India Institute of Technology"
    department: Optional[str] = "Computer Science & Engineering"
    graduation_year: Optional[int] = 2026
    skills: Optional[List[str]] = []

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return sanitize_email(v)

    @field_validator("user_name")
    @classmethod
    def validate_user_name(cls, v: str) -> str:
        return sanitize_text(v, max_length=100, field_name="User Name")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return sanitize_text(v, max_length=128, field_name="Password")

    @field_validator("institution_name")
    @classmethod
    def validate_inst(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_text(v, max_length=150, field_name="Institution") if v else v

    @field_validator("department")
    @classmethod
    def validate_dept(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_text(v, max_length=100, field_name="Department") if v else v

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v: Optional[List[str]]) -> List[str]:
        return sanitize_skills_list(v or [])

class UserLoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return sanitize_email(v, validate_domain=False)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return sanitize_text(v, max_length=128, field_name="Password")

class UserUpdateRequest(BaseModel):
    user_name: Optional[str] = None
    institution_name: Optional[str] = None
    department: Optional[str] = None
    graduation_year: Optional[int] = None

    @field_validator("user_name")
    @classmethod
    def validate_user_name(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_text(v, max_length=100, field_name="User Name") if v else v

    @field_validator("institution_name")
    @classmethod
    def validate_inst(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_text(v, max_length=150, field_name="Institution") if v else v

    @field_validator("department")
    @classmethod
    def validate_dept(cls, v: Optional[str]) -> Optional[str]:
        return sanitize_text(v, max_length=100, field_name="Department") if v else v

class RegistrationResponse(BaseModel):
    success: bool = True
    message: str
    email: str
    email_verified: bool = False

class EmailVerificationRequest(BaseModel):
    token: str

    @field_validator("token")
    @classmethod
    def validate_tok(cls, v: str) -> str:
        return sanitize_text(v, max_length=128, field_name="Verification Token")

class EmailVerificationResponse(BaseModel):
    success: bool
    message: str
    email: Optional[str] = None

class ResendVerificationRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return sanitize_email(v)

class UserResponse(BaseModel):
    id: str
    email: str
    user_name: str
    role: str
    institution_name: Optional[str] = None
    department: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: List[str] = []
    email_verified: bool = True

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class SkillGapCohortItem(BaseModel):
    skill: str
    students_missing_pct: float
    frequency: int
    industry_demand: str
    priority: str

class CurriculumSubjectAudit(BaseModel):
    subject: str
    alignment_score: float
    gap_summary: str
    industry_benchmark: str

class CurriculumElectiveRecommendation(BaseModel):
    title: str
    duration_weeks: int
    target_skills: List[str]
    impact_pct: float
    rationale: str

class InstitutionAnalyticsResponse(BaseModel):
    institution_name: str
    total_students_analyzed: int
    curriculum_alignment_score: float
    placement_readiness: Dict[str, float]
    top_aggregate_skill_gaps: List[SkillGapCohortItem]
    subject_alignment_audit: List[CurriculumSubjectAudit]
    recommended_electives: List[CurriculumElectiveRecommendation]
