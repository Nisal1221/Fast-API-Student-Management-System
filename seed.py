import asyncio
from app.database import Base, engine, AsyncSessionLocal
from app.students.models import Student
from app.courses.models import Course
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")