from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
# We import the association table so SQLAlchemy knows how to join the tables
from app.students.models import student_course_association

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Course code (e.g., "CS101") should be unique and indexed for fast filtering
    code = Column(String(10), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False, default=3)

    # Relationships
    # 'secondary' points to the shared association table mapping rows together.
    # 'back_populates' syncs this directly with the 'courses' attribute on the Student class.
    students = relationship(
        "Student",
        secondary=student_course_association,
        back_populates="courses"
    )

    def __repr__(self):
        return f"<Course {self.code}: {self.title}>"
