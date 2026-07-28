from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.courses.models import Course
from app.courses.schemas import CourseCreate, CourseUpdate, CourseResponse
from app.students.models import Student
from app.auth.utils import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# ==========================================
# 1. CREATE A NEW COURSE
# ==========================================
@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Creates a new course entry in the system."""
    # Check if course code already exists
    query = await db.execute(select(Course).where(Course.code == course_data.code))
    if query.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail=f"Course with code '{course_data.code}' already exists."
        )

    new_course = Course(**course_data.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

# ==========================================
# 2. READ ALL COURSES (PAGINATED)
# ==========================================
@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Fetches a paginated list of all available courses."""
    result = await db.execute(select(Course).offset(skip).limit(limit))
    courses = result.scalars().all()
    return courses

# ==========================================
# 3. READ SINGLE COURSE BY ID
# ==========================================
@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Fetches details for a specific course by its primary ID key."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return course

# ==========================================
# 4. UPDATE A COURSE
# ==========================================
@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Updates an existing course dynamically."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    update_dict = course_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)
    return course

# ==========================================
# 5. DELETE A COURSE
# ==========================================
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Deletes a course and cleans up all associated enrollment mappings."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    await db.delete(course)
    await db.commit()
    return None


# ==========================================
# 6. ENROLLMENT ENDPOINTS (THE LINKING MECHANISM)
# ==========================================

@router.post("/{course_id}/enroll/{student_id}", response_model=CourseResponse)
async def enroll_student(
    course_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Enrolls a specific student into a specific course using their IDs."""
    # Fetch Course
    course_query = await db.execute(select(Course).where(Course.id == course_id))
    course = course_query.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    # Fetch Student
    student_query = await db.execute(select(Student).where(Student.id == student_id))
    student = student_query.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Check if already enrolled
    if student in course.students:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course.")

    # Append relationship via SQLAlchemy ORM
    course.students.append(student)
    await db.commit()
    await db.refresh(course)
    return course


@router.delete("/{course_id}/unenroll/{student_id}", response_model=CourseResponse)
async def unenroll_student(
    course_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    """Removes a student's enrollment from a specific course."""
    # Fetch Course
    course_query = await db.execute(select(Course).where(Course.id == course_id))
    course = course_query.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    # Fetch Student
    student_query = await db.execute(select(Student).where(Student.id == student_id))
    student = student_query.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Check if enrolled
    if student not in course.students:
        raise HTTPException(status_code=400, detail="Student is not currently enrolled in this course.")

    # Remove relationship
    course.students.remove(student)
    await db.commit()
    await db.refresh(course)
    return course
