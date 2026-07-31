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

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest
):
    with span("auth.validate"):

        db: Session = SessionLocal()

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
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

        return {
            "message": "User Registered Successfully"
        }


@router.post("/login")
def login(
    request: LoginRequest
):
    with span("auth.validate"):

        db: Session = SessionLocal()

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:
            return {
                "message": "Invalid Credentials"
            }

        if not verify_password(
            request.password,
            user.hashed_password
        ):
            return {
                "message": "Invalid Credentials"
            }

        return {
            "message": "Login Successful"
        }