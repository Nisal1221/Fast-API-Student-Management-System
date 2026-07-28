from pydantic import BaseModel
from typing import List, Optional

# Base properties shared across schemas
class CourseBase(BaseModel):
    code: str
    title: str
    credits: int

# Schema for creating a new course
class CourseCreate(CourseBase):
    pass

# Schema for updating course details (all fields optional)
class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    credits: Optional[int] = None

# Minimalist student schema nested inside the detailed course response
class StudentMinResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

# Complete API response output for a Course
class CourseResponse(CourseBase):
    id: int
    students: List[StudentMinResponse] = []  # Shows all enrolled students

    class Config:
        from_attributes = True