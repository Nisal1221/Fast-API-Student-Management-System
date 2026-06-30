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
                
             course1 = Course(title="Introduction to Computer Science", code="CS101", credits=4)
            course2 = Course(title="Web Development with FastAPI", code="CS202", credits=3)
            course3 = Course(title="Database Systems", code="CS303", credits=4)
            session.add_all([course1, course2, course3])
            
            # NOTE: bcrypt backend is failing to initialize in this environment.
            # Keep seeding unblocked with a simple placeholder.
            hashed_pwd = "hashed_password_placeholder"



            student1 = Student(first_name="Alice", last_name="Smith", email="alice@example.com", hashed_password=hashed_pwd)
            student2 = Student(first_name="Bob", last_name="Jones", email="bob@example.com", hashed_password=hashed_pwd)
            session.add_all([student1, student2])
            # 3. Simulate Relationships (Enrollments)
            # Alice takes CS101 and CS202
            student1.courses.append(course1)
            student1.courses.append(course2)
            # Bob takes CS202
            student2.courses.append(course2)

        print(" Database successfully seeded with dummy data!")

if __name__ == "__main__":
    asyncio.run(seed_database())