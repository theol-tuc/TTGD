import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)

def install_requirements():
    """Install required packages from requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("Error: requirements.txt not found.")
        sys.exit(1)
    
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    try:
        test_script = Path(__file__).parent / "run_tests.py"
        subprocess.check_call([sys.executable, str(test_script)])
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

def main():
    """Main setup function."""
    print("Setting up Turing Tumble AI Challenge Solver...")
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Run tests
    run_tests()
    
    print("\nSetup completed successfully!")
    print("\nYou can now use the solver by importing from TTG_Backend:")
    print("from TTG_Backend.solver import solve_challenge")
    print("from TTG_Backend.challenges import CHALLENGES")

if __name__ == "__main__":
    main() 