from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class CourseMinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    credits: int


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    courses: List[CourseMinResponse] = []
