from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import List, Optional

#shared properties

class StudentBase(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    
    
#response schema for reading student data

class StudentResponse(StudentBase):
    id:int
    created_at:datetime
    
    class Config:
        orm_mode=True
    
#schema for updating a student record

class StudentUpdate(BaseModel):
    first_name:Optional[str] = None
    last_name:Optional[str]=None
    email:Optional[EmailStr]=None
    
