@echo off
cd /d "e:\Recover 2\Projects\Upwork\Fast API Studet Management System\Fast-API-Student-Management-System"

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else (
  echo .venv not found. Create it with: python -m venv .venv
)

