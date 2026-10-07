"""
CareerPath AI - Authentication & JWT Service
Build For Bharat 2.0 | Intelligent Talent & Workforce Ecosystem

Features:
- Cryptographic PBKDF2-SHA256 password hashing (100,000 rounds with random salt)
- Stateless JWT issuance & signature verification using PyJWT
- Supabase persistence with dual-mode storage (dedicated columns or JSONB metadata)
- Multi-role support: "candidate" (students/jobseekers) and "institution_admin" (universities)
"""

import os
import sys
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
import logging

from backend.config import settings
from backend.database import get_supabase
from backend.models.schemas import (
    UserRegisterRequest, UserLoginRequest, UserUpdateRequest, 
    AuthResponse, UserResponse, RegistrationResponse, EmailVerificationResponse
)
from backend.services.email_service import send_verification_email

logger = logging.getLogger("AuthService")

# JWT Configuration
JWT_SECRET = getattr(settings, "JWT_SECRET", "careerpath_ai_bharat_2026_super_secret_jwt_key_98234")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 72

# ==============================================================================
# 1. CRYPTOGRAPHIC PASSWORD HASHING (PBKDF2-SHA256)
# ==============================================================================
def hash_password(password: str) -> str:
    """Hashes a password with a unique salt using 100,000 iterations of PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${key}"

def verify_password(plain_password: str, hashed_str: str) -> bool:
    """Verifies a plain password against the stored salt$hash string."""
    try:
        if not hashed_str or "$" not in hashed_str:
            return False
        salt, expected_key = hashed_str.split("$", 1)
        actual_key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(actual_key, expected_key)
    except Exception as e:
        logger.warning(f"Password verification error: {e}")
        return False

# ==============================================================================
# 2. JWT TOKEN GENERATION & DECODING
# ==============================================================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Encodes a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=JWT_EXPIRATION_HOURS))
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT token signature and expiration."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None

# ==============================================================================
# 3. USER MANAGEMENT & SUPABASE PERSISTENCE
# ==============================================================================
# Local memory cache for dynamic registered accounts and verification tokens
_LOCAL_USERS_DB: Dict[str, dict] = {}
_VERIFICATION_TOKENS: Dict[str, dict] = {}
_RESEND_COOLDOWNS: Dict[str, datetime] = {}

def create_verification_token(email: str, user_id: str) -> str:
    """Generates a cryptographically secure, time-limited verification token."""
    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=30)

    # Invalidate previous unused tokens for this email
    for t, data in list(_VERIFICATION_TOKENS.items()):
        if data.get("email") == email:
            data["used"] = True

    _VERIFICATION_TOKENS[token] = {
        "token": token,
        "email": email,
        "user_id": user_id,
        "expires_at": expires_at,
        "used": False,
        "created_at": now
    }

    # Store in Supabase if connected
    supabase = get_supabase()
    if supabase:
        try:
            curr = supabase.table("user_profiles").select("experience").eq("id", user_id).execute()
            if curr.data:
                exp = curr.data[0].get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                auth_data["verification_token"] = token
                auth_data["verification_token_expires_at"] = expires_at.isoformat()
                exp["auth"] = auth_data
                supabase.table("user_profiles").update({"experience": exp}).eq("id", user_id).execute()
        except Exception as e:
            logger.warning(f"Could not persist verification token to Supabase: {e}")

    return token

def verify_email_token(token: str) -> EmailVerificationResponse:
    """Validates verification token, activates user account, and invalidates token."""
    if not token or not token.strip():
        raise ValueError("Verification token is missing.")

    token_clean = token.strip()
    now = datetime.now(timezone.utc)
    token_data = _VERIFICATION_TOKENS.get(token_clean)
    email = None
    user_id = None

    if token_data:
        if token_data.get("used"):
            raise ValueError("This verification link has already been used. Please sign in.")
        if now > token_data["expires_at"]:
            raise ValueError("This verification link has expired (valid for 30 minutes). Please request a new verification email.")
        email = token_data["email"]
        user_id = token_data["user_id"]
        token_data["used"] = True
    else:
        # Check Supabase records
        supabase = get_supabase()
        if supabase:
            try:
                resp = supabase.table("user_profiles").select("*").execute()
                for row in resp.data or []:
                    exp = row.get("experience") or {}
                    auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                    if auth_data.get("verification_token") == token_clean:
                        exp_str = auth_data.get("verification_token_expires_at")
                        if exp_str:
                            exp_time = datetime.fromisoformat(exp_str)
                            if now > exp_time:
                                raise ValueError("This verification link has expired. Please request a new verification email.")
                        email = row["email"]
                        user_id = str(row["id"])
                        auth_data["verification_token"] = None
                        auth_data["email_verified"] = True
                        exp["auth"] = auth_data
                        supabase.table("user_profiles").update({"experience": exp}).eq("id", user_id).execute()
                        break
            except Exception as e:
                logger.warning(f"Supabase token lookup error: {e}")

    if not email:
        raise ValueError("Invalid verification token. Please verify the URL or request a new email.")

    # Mark user verified in local cache
    if email in _LOCAL_USERS_DB:
        _LOCAL_USERS_DB[email]["email_verified"] = True

    # Mark user verified in Supabase
    supabase = get_supabase()
    if supabase and user_id:
        try:
            curr = supabase.table("user_profiles").select("experience").eq("id", user_id).execute()
            if curr.data:
                exp = curr.data[0].get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                auth_data["email_verified"] = True
                auth_data["verification_token"] = None
                exp["auth"] = auth_data
                supabase.table("user_profiles").update({"experience": exp}).eq("id", user_id).execute()
        except Exception as e:
            logger.warning(f"Could not update verified flag in Supabase: {e}")

    return EmailVerificationResponse(
        success=True,
        message="Email verified successfully! Your account is now active and you can sign in.",
        email=email
    )

def resend_verification_email(email: str) -> dict:
    """Generates a new verification token and resends email with cooldown enforcement."""
    email_clean = email.strip().lower()
    now = datetime.now(timezone.utc)

    # Enforce 60-second cooldown
    if email_clean in _RESEND_COOLDOWNS:
        elapsed = (now - _RESEND_COOLDOWNS[email_clean]).total_seconds()
        if elapsed < 60:
            remaining = int(60 - elapsed)
            raise ValueError(f"Please wait {remaining} seconds before requesting another verification email.")

    user_record = None
    if email_clean in _LOCAL_USERS_DB:
        user_record = _LOCAL_USERS_DB[email_clean]
    else:
        supabase = get_supabase()
        if supabase:
            try:
                resp = supabase.table("user_profiles").select("*").eq("email", email_clean).execute()
                if resp.data:
                    row = resp.data[0]
                    exp = row.get("experience") or {}
                    auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                    user_record = {
                        "id": str(row["id"]),
                        "email": row["email"],
                        "user_name": row.get("user_name", "Student"),
                        "email_verified": auth_data.get("email_verified", False)
                    }
            except Exception:
                pass

    _RESEND_COOLDOWNS[email_clean] = now

    if user_record and user_record.get("email_verified", False):
        return {
            "success": True,
            "message": "This email address is already verified. You can log in directly."
        }

    if user_record:
        token = create_verification_token(email_clean, user_record["id"])
        send_verification_email(email_clean, user_record.get("user_name", "Student"), token)

    return {
        "success": True,
        "message": "If an unverified account exists for this email, a new verification link has been sent."
    }

def register_user(req: UserRegisterRequest) -> RegistrationResponse:
    email_clean = req.email.strip().lower()
    supabase = get_supabase()

    # 1. Check if email already exists
    if email_clean in _LOCAL_USERS_DB:
        existing = _LOCAL_USERS_DB[email_clean]
        if existing.get("email_verified", False):
            raise ValueError("An account with this email address already exists. Please log in.")
        # If unverified, update password & details, generate fresh token and resend
        pwd_hash = hash_password(req.password)
        existing["password_hash"] = pwd_hash
        existing["user_name"] = req.user_name.strip()
        existing["role"] = req.role
        token = create_verification_token(email_clean, existing["id"])
        send_verification_email(email_clean, existing.get("user_name", req.user_name.strip()), token)
        _RESEND_COOLDOWNS[email_clean] = datetime.now(timezone.utc)
        return RegistrationResponse(
            success=True,
            message="An unverified account with this email already exists. A fresh verification link has been sent to your email.",
            email=email_clean,
            email_verified=False
        )

    if supabase:
        try:
            existing = supabase.table("user_profiles").select("id, experience").eq("email", email_clean).execute()
            if existing.data:
                row = existing.data[0]
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                if auth_data.get("email_verified", False):
                    raise ValueError("An account with this email address already exists. Please log in.")
                pwd_hash = hash_password(req.password)
                auth_data["password_hash"] = pwd_hash
                auth_data["email_verified"] = False
                exp["auth"] = auth_data
                supabase.table("user_profiles").update({
                    "user_name": req.user_name.strip(),
                    "experience": exp
                }).eq("id", row["id"]).execute()
                _LOCAL_USERS_DB[email_clean] = {
                    "id": str(row["id"]),
                    "email": email_clean,
                    "user_name": req.user_name.strip(),
                    "password_hash": pwd_hash,
                    "email_verified": False,
                    "role": req.role
                }
                token = create_verification_token(email_clean, str(row["id"]))
                send_verification_email(email_clean, req.user_name.strip(), token)
                _RESEND_COOLDOWNS[email_clean] = datetime.now(timezone.utc)
                return RegistrationResponse(
                    success=True,
                    message="An unverified account with this email already exists. A fresh verification link has been sent to your email.",
                    email=email_clean,
                    email_verified=False
                )
        except Exception as e:
            if "already exists" in str(e):
                raise e

    # 2. Hash password & prepare record
    pwd_hash = hash_password(req.password)
    user_id = str(uuid.uuid4())

    user_record = {
        "id": user_id,
        "email": email_clean,
        "user_name": req.user_name.strip(),
        "password_hash": pwd_hash,
        "role": req.role,
        "institution_name": req.institution_name,
        "department": req.department,
        "graduation_year": req.graduation_year,
        "skills": req.skills or [],
        "email_verified": False,
        "education": [{"degree": "B.Tech", "department": req.department, "year": req.graduation_year}],
        "experience": {
            "auth": {
                "password_hash": pwd_hash,
                "role": req.role,
                "institution_name": req.institution_name,
                "department": req.department,
                "graduation_year": req.graduation_year,
                "email_verified": False
            }
        }
    }

    # Store locally
    _LOCAL_USERS_DB[email_clean] = user_record

    # Store in Supabase
    if supabase:
        try:
            payload = {
                "id": user_id,
                "user_name": req.user_name.strip(),
                "email": email_clean,
                "skills": req.skills or [],
                "education": user_record["education"],
                "experience": user_record["experience"]
            }
            supabase.table("user_profiles").insert(payload).execute()
        except Exception as e:
            logger.warning(f"Could not persist user to Supabase: {e}")

    # 3. Create verification token & dispatch verification email
    token = create_verification_token(email_clean, user_id)
    send_verification_email(email_clean, req.user_name.strip(), token)
    _RESEND_COOLDOWNS[email_clean] = datetime.now(timezone.utc)

    # CRITICAL: Do NOT issue JWT. Return registration confirmation with email_verified=False
    return RegistrationResponse(
        success=True,
        message="Account created! Please check your email and click the verification link to activate your account.",
        email=email_clean,
        email_verified=False
    )

def login_user(req: UserLoginRequest) -> AuthResponse:
    email_clean = req.email.strip().lower()
    supabase = get_supabase()
    user_record = None

    # Check local DB
    if email_clean in _LOCAL_USERS_DB:
        user_record = _LOCAL_USERS_DB[email_clean]
    elif supabase:
        try:
            resp = supabase.table("user_profiles").select("*").eq("email", email_clean).execute()
            if resp.data:
                row = resp.data[0]
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                pwd_hash = row.get("password_hash") or auth_data.get("password_hash")
                role = row.get("role") or auth_data.get("role", "candidate")
                inst = row.get("institution_name") or auth_data.get("institution_name", "IIT Madras")
                dept = auth_data.get("department", "Computer Science & Engineering")
                grad_yr = auth_data.get("graduation_year", 2026)
                is_verified = row.get("email_verified") if "email_verified" in row else auth_data.get("email_verified", False)

                user_record = {
                    "id": str(row["id"]),
                    "email": row["email"],
                    "user_name": row["user_name"] or "User",
                    "password_hash": pwd_hash,
                    "role": role,
                    "institution_name": inst,
                    "department": dept,
                    "graduation_year": grad_yr,
                    "skills": row.get("skills") or [],
                    "email_verified": is_verified
                }
                _LOCAL_USERS_DB[email_clean] = user_record
        except Exception as e:
            logger.warning(f"Supabase user lookup failed: {e}")

    if not user_record:
        raise ValueError("Invalid email or password.")

    if not verify_password(req.password, user_record.get("password_hash", "")):
        raise ValueError("Invalid email or password.")

    # CRITICAL SECURITY CHECK: Block unverified accounts from logging in or receiving JWT
    if not user_record.get("email_verified", False):
        raise ValueError(
            "Please verify your email address before logging in. Check your inbox for the verification link."
        )

    token = create_access_token({
        "sub": user_record["id"],
        "email": email_clean,
        "role": user_record.get("role", "candidate"),
        "name": user_record.get("user_name", "")
    })

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user_record["id"],
            email=email_clean,
            user_name=user_record.get("user_name", "User"),
            role=user_record.get("role", "candidate"),
            institution_name=user_record.get("institution_name"),
            department=user_record.get("department"),
            graduation_year=user_record.get("graduation_year"),
            skills=[],
            email_verified=True
        )
    )

def get_current_user(token: str) -> Optional[UserResponse]:
    payload = decode_access_token(token)
    if not payload:
        return None
    email = payload.get("email", "").lower()
    if email in _LOCAL_USERS_DB:
        u = _LOCAL_USERS_DB[email]
        return UserResponse(
            id=u["id"],
            email=u["email"],
            user_name=u["user_name"],
            role=u.get("role", "candidate"),
            institution_name=u.get("institution_name"),
            department=u.get("department"),
            graduation_year=u.get("graduation_year"),
            skills=[]
        )
    
    supabase = get_supabase()
    if supabase:
        try:
            resp = supabase.table("user_profiles").select("*").eq("email", email).execute()
            if resp.data:
                row = resp.data[0]
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                user_res = UserResponse(
                    id=str(row["id"]),
                    email=row["email"],
                    user_name=row["user_name"] or "User",
                    role=row.get("role") or auth_data.get("role", "candidate"),
                    institution_name=row.get("institution_name") or auth_data.get("institution_name", "Other Indian University / Institute"),
                    department=auth_data.get("department", "Computer Science & Engineering"),
                    graduation_year=auth_data.get("graduation_year", 2026),
                    skills=[]
                )
                _LOCAL_USERS_DB[email] = {
                    "id": user_res.id,
                    "email": user_res.email,
                    "user_name": user_res.user_name,
                    "role": user_res.role,
                    "institution_name": user_res.institution_name,
                    "department": user_res.department,
                    "graduation_year": user_res.graduation_year,
                    "skills": []
                }
                return user_res
        except Exception as e:
            logger.warning(f"Error fetching user from Supabase: {e}")

    # Fallback to cryptographically validated claims inside token payload
    if payload.get("sub") and email:
        fallback_user = UserResponse(
            id=str(payload.get("sub")),
            email=email,
            user_name=payload.get("name") or "User",
            role=payload.get("role", "candidate"),
            institution_name="Other Indian University / Institute",
            department="Computer Science & Engineering",
            graduation_year=2026,
            skills=[]
        )
        _LOCAL_USERS_DB[email] = {
            "id": fallback_user.id,
            "email": fallback_user.email,
            "user_name": fallback_user.user_name,
            "role": fallback_user.role,
            "institution_name": fallback_user.institution_name,
            "department": fallback_user.department,
            "graduation_year": fallback_user.graduation_year,
            "skills": []
        }
        return fallback_user

    return None

def update_user_profile(user_id: str, req: UserUpdateRequest) -> UserResponse:
    supabase = get_supabase()
    matched_email = None

    # Update local in-memory cache
    for em, u in _LOCAL_USERS_DB.items():
        if u.get("id") == user_id:
            matched_email = em
            if req.user_name is not None and req.user_name.strip():
                u["user_name"] = req.user_name.strip()
            if req.institution_name is not None and req.institution_name.strip():
                u["institution_name"] = req.institution_name.strip()
            if req.department is not None and req.department.strip():
                u["department"] = req.department.strip()
            if req.graduation_year is not None:
                u["graduation_year"] = req.graduation_year
            break

    # Update in Supabase
    if supabase:
        try:
            updates: Dict[str, Any] = {}
            if req.user_name is not None and req.user_name.strip():
                updates["user_name"] = req.user_name.strip()

            curr = supabase.table("user_profiles").select("*").eq("id", user_id).execute()
            if curr.data:
                row = curr.data[0]
                matched_email = row.get("email")
                exp = row.get("experience") or {}
                auth_data = exp.get("auth") if isinstance(exp, dict) else {}
                
                if req.institution_name is not None and req.institution_name.strip():
                    auth_data["institution_name"] = req.institution_name.strip()
                if req.department is not None and req.department.strip():
                    auth_data["department"] = req.department.strip()
                if req.graduation_year is not None:
                    auth_data["graduation_year"] = req.graduation_year

                exp["auth"] = auth_data
                updates["experience"] = exp
                updates["education"] = [{"degree": "B.Tech", "department": auth_data.get("department", "CSE"), "year": auth_data.get("graduation_year", 2026)}]
                
                supabase.table("user_profiles").update(updates).eq("id", user_id).execute()

                # Sync into local cache
                if matched_email:
                    _LOCAL_USERS_DB[matched_email] = {
                        "id": user_id,
                        "email": matched_email,
                        "user_name": updates.get("user_name", row.get("user_name", "User")),
                        "role": row.get("role") or auth_data.get("role", "candidate"),
                        "institution_name": auth_data.get("institution_name", req.institution_name),
                        "department": auth_data.get("department", req.department),
                        "graduation_year": auth_data.get("graduation_year", req.graduation_year),
                        "skills": row.get("skills") or []
                    }
        except Exception as e:
            logger.warning(f"Error updating user profile in Supabase: {e}")

    # Return refreshed user record
    if matched_email and matched_email in _LOCAL_USERS_DB:
        u = _LOCAL_USERS_DB[matched_email]
        return UserResponse(
            id=u["id"],
            email=u["email"],
            user_name=u["user_name"],
            role=u.get("role", "candidate"),
            institution_name=u.get("institution_name"),
            department=u.get("department"),
            graduation_year=u.get("graduation_year"),
            skills=[]
        )

    return UserResponse(
        id=user_id,
        email=matched_email or "user@careerpath.ai",
        user_name=req.user_name or "User",
        role="candidate",
        institution_name=req.institution_name or "Other Indian University / Institute",
        department=req.department or "Computer Science & Engineering",
        graduation_year=req.graduation_year or 2026,
        skills=[]
    )
