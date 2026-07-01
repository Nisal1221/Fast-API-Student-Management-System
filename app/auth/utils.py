from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchmey.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.students.models import Student

#securuty config

SECRET_KEY = "SUPER_SECRET_SECURITY_KEY_KEEP_IT_HIDDEN"  # Change this to a secure random key in productione
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#password hashing confic using bycript
pws_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI where to look for the token (the /auth/login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 2. PASSWORD HASHING UTILITIES

def hash_password(password: str) -> str:
    """Hash a plain-text password using bycript."""
    return pws_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a signed JWT token containing user identity claims."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==========================================
# 4. ROUTE PROTECTION DEPENDENCY
# ==========================================
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> Student:
    """
    Dependency function to secure routes. 
    Decodes the JWT token, verifies it, and fetches the associated user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Asynchronously query the database to make sure the user still exists
    result = await db.execute(select(Student).where(Student.email == email))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user
