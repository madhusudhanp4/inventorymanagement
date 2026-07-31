from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.core.tracing import span

from app.database.database import SessionLocal
from app.models.models import User
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
)
from app.auth.security import (
    hash_password,
    verify_password
)

import time

from app.logging.logging_config import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest
):
    start_time = time.time()

    with span("auth.validate"):

        db: Session = SessionLocal()

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:

            logger.warning(
                "register_failed",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti Madhusudan",
                operation="register",
                duration_ms=int((time.time() - start_time) * 1000),
                status="failure",
                error="user_already_exists",
                request_id="auth",
                extra={
                    "email": request.email
                }
            )

            return {
                "message": "User already exists"
            }

        user = User(
            email=request.email,
            hashed_password=hash_password(
                request.password
            ),
            full_name=request.full_name
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(
            "register_success",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="register",
            duration_ms=int((time.time() - start_time) * 1000),
            status="success",
            error=None,
            request_id="auth",
            extra={
                "email": request.email
            }
        )

        return {
            "message": "User Registered Successfully"
        }



@router.post("/login")
def login(
    request: LoginRequest
):
    start_time = time.time()

    with span("auth.validate"):

        db: Session = SessionLocal()

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:

            logger.warning(
                "login_failed",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti Madhusudan",
                operation="login",
                duration_ms=int((time.time() - start_time) * 1000),
                status="failure",
                error="user_not_found",
                request_id="auth",
                extra={
                    "email": request.email
                }
            )

            return {
                "message": "Invalid Credentials"
            }

        if not verify_password(
            request.password,
            user.hashed_password
        ):

            logger.warning(
                "token_validation_failed",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti Madhusudan",
                operation="auth.validate",
                duration_ms=int((time.time() - start_time) * 1000),
                status="failure",
                error="invalid_password",
                request_id="auth",
                extra={
                    "email": request.email
                }
            )

            return {
                "message": "Invalid Credentials"
            }

        logger.info(
            "login_success",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="login",
            duration_ms=int((time.time() - start_time) * 1000),
            status="success",
            error=None,
            request_id="auth",
            extra={
                "email": request.email
            }
        )

        logger.info(
            "token_validation_success",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="auth.validate",
            duration_ms=int((time.time() - start_time) * 1000),
            status="success",
            error=None,
            request_id="auth",
            extra={
                "email": request.email
            }
        )

        return {
            "message": "Login Successful"
        }