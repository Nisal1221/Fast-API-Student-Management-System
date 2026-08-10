from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.students.models import Student
from app.students.schemas import StudentResponse,StudentUpdate
from app.auth.utils import get_current_user

router=APIRouter(
    prefix="/students",
    tags=["Students"]
)

#reading all students

@router.get("/", response_model=List[StudentResponse])
async def get_students(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user) # Secured
):
    """Fetches a paginated list of all registered students along with their courses."""
    result = await db.execute(select(Student).offset(skip).limit(limit))
    students = result.scalars().all()
    return students

# ==========================================
# 2. READ SINGLE STUDENT BY ID
# ==========================================
@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Retrieves a specific student record by their primary ID key."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found.")
    return student

# ==========================================
# 3. UPDATE STUDENT PROFILE
# ==========================================
@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int, 
    student_data: StudentUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Updates an existing student's data fields dynamically."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found.")
        
    # Apply incoming updates dynamically if they are passed
    update_dict = student_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(student, key, value)
        
    await db.commit()
    await db.refresh(student)
    return student

# ==========================================
# 4. DELETE STUDENT
# ==========================================
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Removes a student profile and auto-clears their associated enrollments."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found.")
        
    await db.delete(student)
    await db.commit()
    return None                                                                                                                                                                                         