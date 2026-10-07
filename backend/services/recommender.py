from backend.models.schemas import RecommendationResponse
from backend.services.gap_analyzer import compute_gap
from backend.services.ml_engine import vector_matcher, salary_predictor

def recommend_roles(user_skills: list[str], user_education: any, user_experience: any, all_roles: list[dict], raw_text: str = "") -> list[RecommendationResponse]:
    recommendations = []
    
    # 1. Train/fit vectorizer on roles corpus
    vector_matcher.fit_corpus(all_roles)
    
    # 2. Build candidate semantic text representation
    skills_text = " ".join(user_skills)
    candidate_doc = f"{skills_text} {skills_text} {raw_text}".strip()
    
    # 3. Compute NLP Cosine Similarities across all roles
    semantic_sim_map = vector_matcher.compute_similarity(candidate_doc)
    
    # Safely extract years of experience
    years_exp = 0.0
    if isinstance(user_experience, dict):
        years_exp = float(user_experience.get("years", 0) or 0.0)
    elif isinstance(user_experience, list) and user_experience:
        years_exp = sum(float(e.get("years", 0.5) if isinstance(e, dict) else 0.5) for e in user_experience)
        
    for role in all_roles:
        rid = str(role.get("id", ""))
        essential_skills = role.get('essential_skills', [])
        optional_skills = role.get('optional_skills', [])
        role_title = role.get("title", "")
        role_cat = role.get("category", "")
        
        # A. Mathematical Skill Gap Fit Score (0-100)
        gap = compute_gap(user_skills, essential_skills, optional_skills, role_title)
        fit_score = gap.fit_score 
        
        # B. NLP Semantic Cosine Similarity (0-100)
        sem_score = semantic_sim_map.get(rid, fit_score)
        
        # C. ML Salary Prediction
        is_ai_or_cloud = "AI" in role_cat or "Cloud" in role_cat or "Machine Learning" in role_title
        essential_ratio = (len(gap.matched_skills) / max(1, len(essential_skills)))
        comp_est = salary_predictor.predict_compensation(
            num_skills=len(user_skills),
            years_exp=years_exp,
            essential_ratio=essential_ratio,
            is_ai_or_cloud=is_ai_or_cloud
        )
        
        # D. Bias-Free Hybrid Multi-Factor Scoring (Skill-First Principle)
        # Evaluates candidate purely on demonstrated competencies, semantic alignment, and practical readiness.
        # Zero penalty for non-traditional education (self-taught, diploma, BCA, bootcamp).
        # 55% Competency Coverage + 35% Semantic Fit + 10% Practical Capability
        readiness_score = min(10.0, max(fit_score * 0.1, years_exp * 2.5))
        
        hybrid_score = (0.55 * fit_score) + (0.35 * sem_score) + (0.10 * readiness_score * 10)
        hybrid_score = round(min(100.0, max(5.0, hybrid_score)), 1)
        
        matched_cnt = len(gap.matched_skills)
        missing_cnt = len(gap.missing_essential)
        
        explanation = (
            f"Semantic Fit: {round(sem_score)}% • Match: {matched_cnt} skill(s). "
            f"Estimated Market Comp: {comp_est['salary_range']}. "
        )
        if missing_cnt > 0:
            explanation += f"Bridge {missing_cnt} essential skill(s) for tier-1 competitiveness."
        else:
            explanation += "Full essential competency alignment verified."
            
        recommendations.append(
            RecommendationResponse(
                role_id=rid,
                role_title=role_title,
                score=hybrid_score,
                explanation=explanation
            )
        )
        
    recommendations.sort(key=lambda x: x.score, reverse=True)
    return recommendations[:12]
