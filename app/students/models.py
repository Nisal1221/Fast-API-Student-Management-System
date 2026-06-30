from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Column

from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ==========================================
# 1. ASSOCIATION (LINK) TABLE
# ==========================================
# This table maps the Many-to-Many relationship between Students and Courses.
# It doesn't need its own class because it's just a helper linking data rows.

student_course_association = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
)

# ==========================================
# 2. STUDENT MODEL
# ==========================================

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True) 
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    # Unique constraints are crucial for production-ready databases
    
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Metadata tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    # This automatically loads associated courses via the link table.
    # 'secondary' tells SQLAlchemy to use the mapping table defined above.
    # 'back_populates' links this to the relationship definition inside the Course model.
    courses = relationship(
        "Course", 
        secondary=student_course_association, 
        back_populates="students"
    )

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"
