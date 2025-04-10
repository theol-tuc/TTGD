@echo off
echo Turing Tumble Test Runner
echo ========================
echo.

cd /d "%~dp0"
echo Current directory: %CD%
echo.

if not exist "test_game.py" (
    echo Error: test_game.py not found in current directory!
    echo Please make sure you're running this from the TTG_Backend directory.
    echo.
    dir
    pause
    exit /b 1
)

if not exist "game_logic.py" (
    echo Error: game_logic.py not found in current directory!
    echo Please make sure you're running this from the TTG_Backend directory.
    echo.
    dir
    pause
    exit /b 1
)

echo Running test...
echo.
python test_game.py

if errorlevel 1 (
    echo.
    echo Error running test. Please check:
    echo 1. Python is installed and in your PATH
    echo 2. You're in the correct directory
    echo 3. All required files are present
    echo.
    dir
)
pause 