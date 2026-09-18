from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    code: str
    title: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    credits: Optional[int] = None


class StudentMinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    students: List[StudentMinResponse] = []