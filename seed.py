import asyncio
from app.database import Base, engine, AsyncSessionLocal
from app.students.models import Student
from app.courses.models import Course
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSessionLocal() as session:
            async with session.begin():