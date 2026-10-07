import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Configure UTF-8 stdout for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

# Add both root and backend directory to sys.path for universal import compatibility
root_dir = Path(__file__).resolve().parent.parent
backend_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import resume, roles, analysis, recommendations, roadmap, report, auth, talent_intelligence
from backend.database import get_supabase
from backend.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Supabase client
    client = get_supabase()
    if client:
        print("✓ Supabase client connected successfully")
    else:
        print("ℹ Supabase credentials not set or pending; operating in resilient real-dataset mode")
    yield

app = FastAPI(
    title="CareerPath AI - Backend API",
    description="Intelligent Talent & Workforce Ecosystem API for Build For Bharat 2.0",
    version="2.0.0",
    lifespan=lifespan
)

# Production & Local CORS settings
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]
if hasattr(settings, "FRONTEND_URL") and settings.FRONTEND_URL:
    allowed_origins.append(settings.FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https://.*(\.vercel\.app|\.netlify\.app|\.pages\.dev|\.onrender\.com)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_defense_middleware(request: Request, call_next):
    # 1. Inspect query parameters for SQL/NoSQL injection signatures
    for param_name, param_val in request.query_params.items():
        val_upper = param_val.upper()
        if any(token in val_upper for token in [
            "UNION SELECT", "DROP TABLE", "INSERT INTO", "DELETE FROM",
            "1=1", "OR '1'='1'", "$WHERE", "$GT", "$NE", "$REGEX", "--", "/*"
        ]):
            return JSONResponse(
                status_code=400,
                content={"detail": f"Security Alert: Malicious SQL/NoSQL pattern detected in parameter '{param_name}'."}
            )

    response = await call_next(request)

    # 2. Add standard HTTP security headers (OWASP)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(roles.router)
app.include_router(analysis.router)
app.include_router(recommendations.router)
app.include_router(roadmap.router)
app.include_router(report.router)
app.include_router(talent_intelligence.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "CareerPath AI", "version": "2.0.0"}

@app.get("/api/ml/metrics")
async def get_ml_metrics():
    import json
    model_file = backend_dir / "data" / "trained_salary_model.json"
    vel_file = backend_dir / "data" / "skill_market_velocity.json"
    roles_file = backend_dir / "data" / "indian_role_benchmarks.json"
    
    metrics = {
        "status": "ready",
        "model": "NumPyRidgeRegressor (Closed-Form Analytical)",
        "datasets": [
            "Indian_Fresher_Salary_Skills_2025.csv (500 rows)",
            "india_job_market_2024_2026.csv (5,000 rows)",
            "indian-job-market-dataset-2025.xlsx (97,000+ listings sampled)",
            "ESCO European Commission Official API (42 roles, 788 skills)"
        ]
    }
    if model_file.exists():
        with open(model_file, "r", encoding="utf-8") as f:
            metrics["salary_model"] = json.load(f)
    if vel_file.exists():
        with open(vel_file, "r", encoding="utf-8") as f:
            v_data = json.load(f)
            metrics["tracked_skills_count"] = len(v_data)
    if roles_file.exists():
        with open(roles_file, "r", encoding="utf-8") as f:
            r_data = json.load(f)
            metrics["empirical_indian_roles_count"] = len(r_data)
            
    return metrics

if __name__ == "__main__":
    import uvicorn
    # Watch only source folders excluding .venv to enable instant live updates
    watch_dirs = [
        str(backend_dir / "routers"),
        str(backend_dir / "services"),
        str(backend_dir / "models")
    ]
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=watch_dirs)
