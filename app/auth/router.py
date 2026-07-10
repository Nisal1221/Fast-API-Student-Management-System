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
    """
    Registers a new student, hashes their password, and immediately logs them in 
    by returning a valid JWT access token.to Depends(get_db).
    
    """
    query = await db.execute(select(Student).where(Student.email == user_data.email))
    excisting_user = query.scalars().first()
    
    if excisting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
            )
    
    #password hashing & save new user to the database
    
    hashed_pwd = hash_password(user_data.password)
    new_student = Student(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    
    #Auto loging the user post reg
    
    access_token = create_access_token(data={"sub":new_student.email})
    return{"access_token": access_token, "token_type":"bearer"}

@router.post("/login", response_model=TokoenResponse)
async def login_student(
    from_data:OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
): 
    """
    Authenticates a student using standerd OAuth2password flow. If the credentials are valid, returns a JWT access token if credintials match.
    """
    #fetch the user from the database
    

    
        