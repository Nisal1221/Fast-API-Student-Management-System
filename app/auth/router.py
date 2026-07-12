from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.students.models import Student

router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def register_student(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    query = await db.execute(select(Student).where(Student.email == user_data.email))
    existing_user = query.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    hashed_pwd = hash_password(user_data.password)
    new_student = Student(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pwd,
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    access_token = create_access_token(data={"sub": new_student.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login_student(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    query = await db.execute(select(Student).where(Student.email == from_data.username))
    student = query.scalars().first()

    invalid_credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not student or not verify_password(from_data.password, student.hashed_password):
        raise invalid_credential_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}

     
        