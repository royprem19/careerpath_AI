import logging
from fastapi import APIRouter, HTTPException
from backend.models.schemas import GapAnalysisRequest, GapAnalysisResponse
from backend.services.gap_analyzer import compute_gap
from backend.routers.roles import get_role
from backend.database import get_supabase

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/api/analysis/gap", response_model=GapAnalysisResponse)
async def analyze_gap(request: GapAnalysisRequest):
    try:
        role = await get_role(request.target_role_id)
        gap = compute_gap(
            user_skills=request.user_skills,
            role_essential_skills=role.essential_skills,
            role_optional_skills=role.optional_skills,
            role_title=role.title,
            role_category=role.category or ""
        )

        # Automatically log/persist gap analysis into Supabase gap_analyses table
        supabase = get_supabase()
        if supabase:
            try:
                numeric_role_id = None
                try:
                    numeric_role_id = int(request.target_role_id)
                except (ValueError, TypeError):
                    pass

                record = {
                    "fit_score": float(gap.fit_score),
                    "essential_coverage": float(gap.essential_coverage),
                    "optional_coverage": float(gap.optional_coverage),
                    "matched_skills": gap.matched_skills or [],
                    "missing_essential": gap.missing_essential or [],
                    "missing_optional": gap.missing_optional or [],
                    "surplus_skills": gap.surplus_skills or []
                }
                if numeric_role_id is not None:
                    record["role_id"] = numeric_role_id

                supabase.table("gap_analyses").insert(record).execute()
                logger.info(f"Successfully saved gap analysis for role '{role.title}' in Supabase gap_analyses table.")
            except Exception as db_err:
                logger.warning(f"Note: Could not persist gap analysis to Supabase: {db_err}")

        return gap
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
