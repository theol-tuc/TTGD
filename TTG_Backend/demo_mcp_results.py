"""
Demo script for the Model Context Protocol (MCP) integration.
This script demonstrates how to use the MCP with the AIChallengeSolver.
"""

from AIChallengeSolver import AIChallengeSolver
from game_logic import ComponentType, BLUE, RED
import json
from datetime import datetime

def create_sample_challenge():
    """Create a sample challenge configuration."""
    return {
        'red_marbles': 1,
        'blue_marbles': 1,
        'components': [
            {'type': 'RAMP_LEFT', 'x': 7, 'y': 1},
            {'type': 'INTERCEPTOR', 'x': 6, 'y': 2}
        ],
        'expected_outputs': {
            BLUE: [(6, 2)],
            RED: []
        }
    }

def run_mcp_demo():
    """Run the MCP demo with a sample challenge."""
    print("Initializing MCP Demo...")
    print("-" * 50)
    
    # Initialize the solver
    solver = AIChallengeSolver()
    
    # Create a sample challenge
    challenge = create_sample_challenge()
    
    print("\nChallenge Configuration:")
    print(json.dumps(challenge, indent=2))
    print("-" * 50)
    
    # Solve the challenge with MCP reporting
    print("\nSolving challenge with MCP reporting...")
    solution = solver.solve_challenge_with_mcp(challenge)
    
    print("\nSolution Steps:")
    print(json.dumps(solution, indent=2))
    print("-" * 50)
    
    # Print success metrics
    print("\nSuccess Metrics:")
    print(f"Success Rate: {solver.get_success_rate():.2%}")
    print(f"Total Attempts: {solver.total_attempts}")
    print(f"Successful Solutions: {solver.success_count}")
    print("-" * 50)

if __name__ == "__main__":
    run_mcp_demo() 