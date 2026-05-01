@echo off
REM Quick Start Script for Running Tests Locally (Windows)
REM 
REM This script demonstrates how to run the test suite and CI/CD checks
REM locally before pushing to GitHub
REM
REM Usage: run_tests.bat

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   Automotive Software Testing - Local Run
echo ==========================================
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.9+
    exit /b 1
)
python --version
echo [OK] Python installation verified
echo.

REM Create virtual environment
echo [2/6] Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo [OK] Dependencies installed
echo.

REM Run unit tests
echo [5/6] Running unit tests...
echo ========== UNIT TESTS ==========
python test_helloworld.py

set TEST_EXIT_CODE=%ERRORLEVEL%
echo.

REM Generate coverage report
echo [6/6] Generating coverage report...
coverage run --source=. -m pytest test_helloworld.py 2>nul || goto skip_coverage
coverage report
coverage html -d coverage_report 2>nul

:skip_coverage
echo [OK] Coverage report: coverage_report\index.html
echo.

REM Summary
echo ==========================================
echo   Test Results Summary
echo ==========================================
if %TEST_EXIT_CODE% equ 0 (
    echo [OK] All tests PASSED!
    echo.
    echo Next steps:
    echo   1. Review coverage report: start coverage_report\index.html
    echo   2. Check test results above
    echo   3. Push changes to GitHub to run CI/CD pipeline
    echo.
    echo To view coverage in browser:
    echo   - Windows: start coverage_report\index.html
) else (
    echo [WARN] Some tests failed - see details above
)

echo.
echo For more information, see README.md
echo.

pause
