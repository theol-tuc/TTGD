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
                elif component.type == ComponentType.LAUNCHER:
                    grid[y][x] = 'L'
    
    # Add marbles
    for marble in board.marbles:
        grid[marble.y][marble.x] = 'O'
    
    # Print the grid
    print('-' * (board.width * 2 + 1))
    for row in grid:
        print('|' + ' '.join(row) + '|')
    print('-' * (board.width * 2 + 1))
    print(f"Score: {board.score}")
    print(f"Active Launcher: {board.active_launcher}")
    print(f"Number of marbles: {len(board.marbles)}")

def main():
    # Create a game board
    board = GameBoard(11, 10)  # Width 11, Height 10
    
    # Add some components for testing
    board.add_component(ComponentType.RAMP_LEFT, 3, 2)
    board.add_component(ComponentType.RAMP_RIGHT, 7, 2)
    board.add_component(ComponentType.INTERCEPTOR, 5, 5)
    
    # Test left launcher
    print("\nTesting left launcher:")
    board.set_active_launcher("left")
    board.launch_marble()
    
    # Simulate a few steps
    for _ in range(8):
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)
    
    # Reset and test right launcher
    print("\nTesting right launcher:")
    board.reset()
    board.add_component(ComponentType.RAMP_LEFT, 3, 2)
    board.add_component(ComponentType.RAMP_RIGHT, 7, 2)
    board.add_component(ComponentType.INTERCEPTOR, 5, 5)
    
    board.set_active_launcher("right")
    board.launch_marble()
    
    # Simulate a few steps
    for _ in range(8):
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)

if __name__ == "__main__":
    main() 