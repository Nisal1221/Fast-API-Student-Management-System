from datetime import timedelta
from fastapi import APIRouter , Depends ,HTTTPexception , status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic importBasemodel , EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.students.models import Student

from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

roter = APIRouter(prefix="/auth" , 
                  tags=["Authentication"]
                  )

# 1. TEMPORARY SCHEMAS FOR DATA VALIDATION

class UserRegister(BaseModel):
    first_name: str
    last_name:str
    email:emailStr
    password:str
        
class TokenResponse(BaseModel):
    access_token:str
    token_type:str 
    
#2. FASTAPI ENDPOINTS
@router.post("/register",status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register_student(user_data: UserRegister , db: asyncSession = Depends(get_db)):
    