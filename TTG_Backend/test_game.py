import sys
import os
import time
from game_logic import GameBoard, ComponentType, Marble

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """Print the current state of the board with borders and marble counts"""
    clear_screen()
    # Create a grid with empty spaces
    grid = [[' ' for _ in range(15)] for _ in range(17)]

    # Add components
    for y in range(17):
        for x in range(15):
            component = board.components[y][x]
            if component.type != ComponentType.EMPTY:
                if component.type == ComponentType.RAMP_LEFT:
                    grid[y][x] = '\\'
                elif component.type == ComponentType.RAMP_RIGHT:
                    grid[y][x] = '/'
                elif component.type == ComponentType.CROSSOVER:
                    grid[y][x] = '+'
                elif component.type == ComponentType.BIT_LEFT:
                    grid[y][x] = 'O'
                elif component.type == ComponentType.INTERCEPTOR:
                    grid[y][x] = 'X'
                elif component.type == ComponentType.LAUNCHER:
                    grid[y][x] = 'L'
                elif component.type == ComponentType.BORDER_VERTICAL:
                    grid[y][x] = '|'
                elif component.type == ComponentType.BORDER_HORIZONTAL:
                    grid[y][x] = '-'
                elif component.type == ComponentType.BORDER_DIAGONAL_LEFT:
                    grid[y][x] = '\\'
                elif component.type == ComponentType.BORDER_DIAGONAL_RIGHT:
                    grid[y][x] = '/'
                elif component.type == ComponentType.CORNER_LEFT:
                    grid[y][x] = '+'
                elif component.type == ComponentType.CORNER_RIGHT:
                    grid[y][x] = '+'
                elif component.type == ComponentType.LEVER_BLUE:
                    grid[y][x] = 'B'
                elif component.type == ComponentType.LEVER_RED:
                    grid[y][x] = 'R'

    # Add marbles with their colors
    for marble in board.marbles:
        grid[marble.y][marble.x] = 'R' if marble.color == "red" else 'B'

    # Print the grid with borders
    print('-' * (15 * 2 + 1))
    for row in grid:
        print('|' + ' '.join(row) + '|')
    print('-' * (15 * 2 + 1))

    # Print marble counts and active launcher
    print(f"Red Marbles: {board.red_marbles}")
    print(f"Blue Marbles: {board.blue_marbles}")
    print(f"Active Launcher: {board.active_launcher}")

def test_scenario_1():
    """Basic test with alternating ramps and proper board setup"""
    print("\n=== Test Scenario 1: Alternating Ramps ===")
    board = GameBoard()

    # Add borders
    for y in range(17):
        board.add_component(ComponentType.BORDER_VERTICAL, 0, y)
        board.add_component(ComponentType.BORDER_VERTICAL, 14, y)
    for x in range(15):
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 0)
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 16)

    # Add launchers at top
    board.add_component(ComponentType.LAUNCHER, 3, 0)  # Left launcher
    board.add_component(ComponentType.LAUNCHER, 11, 0)  # Right launcher

    # Add alternating ramps
    for y in range(2, 15, 2):
        board.add_component(ComponentType.RAMP_LEFT, 5, y)
        board.add_component(ComponentType.RAMP_RIGHT, 9, y)

    # Add interceptors at bottom
    board.add_component(ComponentType.INTERCEPTOR, 3, 16)  # Left interceptor
    board.add_component(ComponentType.INTERCEPTOR, 11, 16)  # Right interceptor

    print_board(board)
    return board

def test_scenario_2():
    """Test with bits, crossovers, and proper board setup"""
    print("\n=== Test Scenario 2: Bits and Crossovers ===")
    board = GameBoard()

    # Add borders
    for y in range(17):
        board.add_component(ComponentType.BORDER_VERTICAL, 0, y)
        board.add_component(ComponentType.BORDER_VERTICAL, 14, y)
    for x in range(15):
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 0)
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 16)

    # Add launchers at top
    board.add_component(ComponentType.LAUNCHER, 3, 0)  # Left launcher
    board.add_component(ComponentType.LAUNCHER, 11, 0)  # Right launcher

    # Add bits in a pattern
    for y in range(3, 12, 3):
        board.add_component(ComponentType.BIT_LEFT, 4, y)
        board.add_component(ComponentType.BIT_RIGHT, 10, y)

    # Add crossovers
    board.add_component(ComponentType.CROSSOVER, 7, 6)
    board.add_component(ComponentType.CROSSOVER, 7, 9)

    # Add interceptors at bottom
    board.add_component(ComponentType.INTERCEPTOR, 3, 16)  # Left interceptor
    board.add_component(ComponentType.INTERCEPTOR, 11, 16)  # Right interceptor

    print_board(board)
    return board

def test_scenario_3():
    """Test with a complex pattern and proper board setup"""
    print("\n=== Test Scenario 3: Complex Pattern ===")
    board = GameBoard()

    # Add borders
    for y in range(17):
        board.add_component(ComponentType.BORDER_VERTICAL, 0, y)
        board.add_component(ComponentType.BORDER_VERTICAL, 14, y)
    for x in range(15):
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 0)
        board.add_component(ComponentType.BORDER_HORIZONTAL, x, 16)

    # Add launchers at top
    board.add_component(ComponentType.LAUNCHER, 3, 0)  # Left launcher
    board.add_component(ComponentType.LAUNCHER, 11, 0)  # Right launcher

    # Create a zigzag pattern with ramps
    for y in range(2, 13, 2):
        if y % 4 == 2:
            board.add_component(ComponentType.RAMP_LEFT, 5, y)
            board.add_component(ComponentType.RAMP_RIGHT, 9, y)
        else:
            board.add_component(ComponentType.RAMP_RIGHT, 5, y)
            board.add_component(ComponentType.RAMP_LEFT, 9, y)

    # Add bits at strategic points
    board.add_component(ComponentType.BIT_LEFT, 4, 7)
    board.add_component(ComponentType.BIT_RIGHT, 10, 7)

    # Add interceptors at bottom
    board.add_component(ComponentType.INTERCEPTOR, 3, 16)  # Left interceptor
    board.add_component(ComponentType.INTERCEPTOR, 11, 16)  # Right interceptor

    print_board(board)
    return board

def run_test_scenario(board):
    """Run a test scenario with marbles"""
    print("\nRunning test scenario...")
    time.sleep(1)

    # Test left launcher (blue marbles)
    print("\nLaunching blue marbles from left:")
    board.set_active_launcher("left")
    for marble_num in range(3):
        print(f"\nLaunching blue marble {marble_num + 1}...")
        board.launch_marble("blue")
        # Wait for marble to settle
        steps = 0
        while board.marbles:
            board.update_marble_positions()
            print_board(board)
            print(f"Step {steps + 1}: Marble is moving...")
            time.sleep(0.5)  # Increased delay for better visibility
            steps += 1
        print(f"Blue marble {marble_num + 1} settled. Count: {board.blue_marbles}")
        time.sleep(1)  # Pause between marbles

    # Test right launcher (red marbles)
    print("\nLaunching red marbles from right:")
    board.set_active_launcher("right")
    for marble_num in range(3):
        print(f"\nLaunching red marble {marble_num + 1}...")
        board.launch_marble("red")
        # Wait for marble to settle
        steps = 0
        while board.marbles:
            board.update_marble_positions()
            print_board(board)
            print(f"Step {steps + 1}: Marble is moving...")
            time.sleep(0.5)  # Increased delay for better visibility
            steps += 1
        print(f"Red marble {marble_num + 1} settled. Count: {board.red_marbles}")
        time.sleep(1)  # Pause between marbles

def main():
    """Run all test scenarios"""
    print("Starting Turing Tumble Test Scenarios")
    print("="*50)

    # Run each scenario
    scenarios = [
        ("Basic Alternating Ramps", test_scenario_1),
        ("Bits and Crossovers", test_scenario_2),
        ("Complex Pattern", test_scenario_3)
    ]

    for name, scenario_func in scenarios:
        print(f"\nRunning {name}...")
        board = scenario_func()
        run_test_scenario(board)
        input("\nPress Enter to continue to next scenario...")

if __name__ == "__main__":
    main() 