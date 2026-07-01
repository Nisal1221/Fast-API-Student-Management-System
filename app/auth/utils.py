from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchmey.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.students.models import Student
