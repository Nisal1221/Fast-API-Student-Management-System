from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.students.models import student_course_association



class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credits = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Back-populated from Student.courses.
    students = relationship(
        "Student",
        secondary=student_course_association,
        back_populates="courses",
    )



    def __repr__(self):
        return f"<Course {self.code} ({self.title})>"

