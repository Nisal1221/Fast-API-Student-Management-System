from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import List, Optional

#shared properties

class StudentBase(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    
#schema for updating a student record

class StudentUpdate(BaseModel):
    first_name:Optional[str] = None
    last_name:Optional[str]=None
    email:Optional[EmailStr]=None
    
