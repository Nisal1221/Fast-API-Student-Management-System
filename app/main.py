from fastAPI import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.auth.router import router as  auth_router
from app.students.router import router as student_router
from app.courses.router import router as course_router

#lifespan event for startup and shutdown

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that runs tasks on startup and shutdown.
    On startup: Automatically creates database tables if they don't exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Initialize FastAPI application with lifespan context

app = FastAPI(
    title="Student Management System API",
    description=(
        "A robust, asynchronous RESTful API for managing students, courses, "
        "and enrollments. Features JWT authentication, relational database "
        "modelling via SQLAlchemy ORM, and automated OpenAPI documentation."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# ==========================================
# 3. CORS MIDDLEWARE CONFIGURATION
# ==========================================
# Allows front-end clients (React, Vue, mobile apps) to communicate with your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production to restrict domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 4. ROUTER REGISTRATION
# ==========================================
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(course_router)


# ==========================================
# 5. ROOT HEALTH CHECK ENDPOINT
# ==========================================
@app.get("/", tags=["Health Check"])
async def root():
    """Simple health check endpoint to confirm API operational status."""
    return {
        "status": "online",
        "message": "Welcome to the Student Management System API!",
        "documentation": "/docs"
    }