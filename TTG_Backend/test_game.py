import sys
import time
from game_logic import GameBoard, ComponentType

def print_board(board: GameBoard) -> None:
    """Print the current state of the board"""
    # Create a grid with empty spaces
    grid = [[' ' for _ in range(board.width)] for _ in range(board.height)]
    
    # Add components
    for y in range(board.height):
        for x in range(board.width):
            component = board.components[y][x]
            if component.type != ComponentType.EMPTY:
                if component.type == ComponentType.RAMP_LEFT:
                    grid[y][x] = '\\'
                elif component.type == ComponentType.RAMP_RIGHT:
                    grid[y][x] = '/'
                elif component.type == ComponentType.CROSSOVER:
                    grid[y][x] = '+'
                elif component.type == ComponentType.INTERCEPTOR:
                    grid[y][x] = 'X'
                elif component.type == ComponentType.RED_LAUNCHER:
                    grid[y][x] = 'R'
                elif component.type == ComponentType.BLUE_LAUNCHER:
                    grid[y][x] = 'L'
    
    # Add marbles with their colors
    for marble in board.marbles:
        grid[marble.y][marble.x] = 'R' if marble.color == "red" else 'B'
    
    # Print the grid
    print('-' * (board.width * 2 + 1))
    for row in grid:
        print('|' + ' '.join(row) + '|')
    print('-' * (board.width * 2 + 1))
    
    # Print marble counts
    counts = board.get_marble_counts()
    print(f"Total Red Marbles: {counts['red']}")
    print(f"Total Blue Marbles: {counts['blue']}")
    print(f"Active Launcher: {board.active_launcher}")

def main():
    # Create a game board
    board = GameBoard(11, 10)  # Width 11, Height 10
    
    # Add some components for testing
    board.add_component(ComponentType.RAMP_LEFT, 3, 2)
    board.add_component(ComponentType.RAMP_RIGHT, 7, 2)
    board.add_component(ComponentType.INTERCEPTOR, 5, 9)  # Place interceptor at bottom middle
    
    # Add launchers at the top
    board.add_component(ComponentType.LAUNCHER, 3, 0)  # Left launcher
    board.add_component(ComponentType.LAUNCHER, 7, 0)  # Right launcher
    
    # Test left launcher with red marble
    print("\nTesting left launcher with red marble:")
    board.set_active_launcher("left")
    board.launch_marble("red")
    
    # Simulate a few steps
    for _ in range(12):  # Increased steps to allow marble to reach bottom
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)
    
    # Wait for all marbles to settle
    while board.marbles:
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)
    
    # Test right launcher with blue marble
    print("\nTesting right launcher with blue marble:")
    board.set_active_launcher("right")
    board.launch_marble("blue")
    
    # Simulate a few steps
    for _ in range(12):  # Increased steps to allow marble to reach bottom
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)
    
    # Wait for all marbles to settle
    while board.marbles:
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)
    
    # Print final counts
    print("\nFinal Marble Counts:")
    counts = board.get_marble_counts()
    print(f"Total Red Marbles: {counts['red']}")
    print(f"Total Blue Marbles: {counts['blue']}")

if __name__ == "__main__":
    main() 