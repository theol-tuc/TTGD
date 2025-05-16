import pytest
import os
import sys

def main():
    # Get the directory containing this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the parent directory to Python path
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    # Run pytest with coverage
    pytest_args = [
        "--cov=TTG_Backend",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/"
    ]
    
    # Run the tests
    exit_code = pytest.main(pytest_args)
    
    # Print coverage report location
    coverage_dir = os.path.join(current_dir, "htmlcov")
    if os.path.exists(coverage_dir):
        print(f"\nCoverage report generated in: {coverage_dir}")
        print("Open index.html in your browser to view the detailed report.")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 