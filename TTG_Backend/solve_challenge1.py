from TTG_Backend.game_logic import GameBoard, ComponentType
from TTG_Backend.AIChallengeSolver import TransformerPlanner

def solve_challenge_1():
    # Create the board
    board = GameBoard()
    
    # Set up the board according to Challenge 1 (Gravity)
    board.set_component(7, 5, ComponentType.RAMP_LEFT)
    board.set_component(7, 7, ComponentType.RAMP_RIGHT)
    board.set_component(7, 3, ComponentType.CROSSOVER)
    board.set_component(6, 4, ComponentType.INTERCEPTOR)
    
    # Create the prompt for GPT-4
    prompt = """
    You are a Turing Tumble puzzle solver.

    Board description:
    - Components:
      - RAMP_LEFT at (7, 5)
      - RAMP_RIGHT at (7, 7)
      - CROSSOVER at (7, 3)
      - INTERCEPTOR at (6, 4)
    - Start position: (0, 0)
    - Goal position: (7, 7)
    - Ball color: BLUE

    Objective: Guide the blue marble from the start to the goal using the components.

    Please provide a step-by-step solution, describing each move or action.
    """
    
    # Initialize the GPT-4 planner
    planner = TransformerPlanner()
    
    # Generate solution plan using GPT-4
    plan = planner.plan(prompt)
    steps = planner.parse_plan(plan)
    
    # Print the solution
    print("\nChallenge 1 (Gravity) Solution:")
    print("----------------------------")
    print("Initial Board State:")
    board.print_board()
    print("\nSolution Steps:")
    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")
    
    # Measure accuracy
    ground_truth = [
        "Move ball to position (7, 5)",
        "Move ball to position (7, 7)"
    ]
    accuracy = measure_accuracy(steps, ground_truth)
    print(f"\nAccuracy: {accuracy:.2f}%")
    
    return steps

def measure_accuracy(predicted_steps, ground_truth):
    """Measure the accuracy of the predicted steps against the ground truth."""
    correct = sum(1 for p, g in zip(predicted_steps, ground_truth) if p == g)
    return (correct / len(ground_truth)) * 100 if ground_truth else 0

if __name__ == "__main__":
    solve_challenge_1() 