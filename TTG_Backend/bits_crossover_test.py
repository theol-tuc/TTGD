import sys
import time
from game_logic import GameBoard, ComponentType


def print_board(board: GameBoard) -> None:
    """Print the current state of the board"""
    # Create a grid with empty spaces
    grid = [[' ' for _ in range(board.width)] for _ in range(board.height)]

    # First, add the components to the grid
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
                elif component.type == ComponentType.BIT_LEFT:
                    grid[y][x] = '<'  # Bit Left visual
                elif component.type == ComponentType.BIT_RIGHT:
                    grid[y][x] = '>'  # Bit Right visual
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

    # Then, add marbles to the grid. But only add the marble if the spot is not a bit.
    for marble in board.marbles:
        if board.components[marble.y][marble.x].type not in [ComponentType.BIT_LEFT, ComponentType.BIT_RIGHT]:
            grid[marble.y][marble.x] = 'R' if marble.color == "red" else 'B'
        # If the marble is on top of a bit, leave the bit symbol (don't overwrite)

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
    # Create a game board with correct dimensions
    board = GameBoard(15, 17)  # Width 15, Height 17

    # Add components for testing
    # re-entry challenge
    board.add_component(ComponentType.RAMP_LEFT, 5, 3)
    board.add_component(ComponentType.RAMP_LEFT, 6, 4)
    board.add_component(ComponentType.RAMP_LEFT, 7, 5)
    board.add_component(ComponentType.RAMP_LEFT, 8, 6)
    board.add_component(ComponentType.RAMP_LEFT, 9, 7)
    board.add_component(ComponentType.RAMP_LEFT, 10, 8)
    board.add_component(ComponentType.RAMP_LEFT, 11, 9)
    board.add_component(ComponentType.RAMP_LEFT, 12, 10)


    #gravity challenge
    # board.add_component(ComponentType.RAMP_LEFT, 6, 3) 
    # board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    # board.add_component(ComponentType.RAMP_RIGHT, 5, 5)
    # board.add_component(ComponentType.RAMP_RIGHT, 4, 6)
    # board.add_component(ComponentType.RAMP_RIGHT, 3, 7)
    # board.add_component(ComponentType.RAMP_RIGHT, 2, 8)

    #tetrad challenge
    # bit_L = ComponentType.BIT_LEFT
    # bit_R = ComponentType.BIT_RIGHT
    # board.add_component(bit_R, 6, 3)
    # board.add_component(bit_L, 5, 4)  
    # board.add_component(bit_R, 6, 5)
    # board.add_component(bit_L, 5, 6)
    # board.add_component(bit_R, 6, 7)    
    # board.add_component(bit_L, 5, 8)
    # board.add_component(bit_R, 6, 9)
    # board.add_component(ComponentType.INTERCEPTOR, 5, 10)

    # board.add_component(ComponentType.CROSSOVER, 5, 8)  
    # board.add_component(ComponentType.BIT_LEFT, 9, 8)  

    # Test sequence 1: Blue marbles from left side
    print("\nTest Sequence 1: Launching 3 blue marbles from left side")
    board.set_active_launcher("left")

    # Launch first blue marble
    print("\nLaunching first blue marble:")
    board.launch_marble("blue")
    for _ in range(20):
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)

    # Wait for marble to settle
    while board.marbles:
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)

    # Launch second blue marble
    print("\nLaunching second blue marble:")
    board.launch_marble("blue")
    for _ in range(20):
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)

    # # Wait for marble to settle
    while board.marbles:
        print_board(board)
        board.update_marble_positions()
        time.sleep(0.5)

    # # Launch third blue marble
    # print("\nLaunching third blue marble:")
    # board.launch_marble("blue")
    # for _ in range(20):
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # Wait for all marbles to settle
    # while board.marbles:
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Print intermediate counts
    # print("\nIntermediate Counts after blue marbles:")
    # counts = board.get_marble_counts()
    # print(f"Total Red Marbles: {counts['red']}")
    # print(f"Total Blue Marbles: {counts['blue']}")

    # # Test sequence 2: Red marbles from right side
    # print("\nTest Sequence 2: Launching 3 red marbles from right side")
    # board.set_active_launcher("right")

    # # Launch first red marble
    # print("\nLaunching first red marble:")
    # board.launch_marble("red")
    # for _ in range(20):
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Wait for marble to settle
    # while board.marbles:
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Launch second red marble
    # print("\nLaunching second red marble:")
    # board.launch_marble("red")
    # for _ in range(20):
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Wait for marble to settle
    # while board.marbles:
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Launch third red marble
    # print("\nLaunching third red marble:")
    # board.launch_marble("red")
    # for _ in range(20):
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Wait for all marbles to settle
    # while board.marbles:
    #     print_board(board)
    #     board.update_marble_positions()
    #     time.sleep(0.5)

    # # Print final counts
    # print("\nFinal Marble Counts:")
    # counts = board.get_marble_counts()
    # print(f"Total Red Marbles: {counts['red']}")
    # print(f"Total Blue Marbles: {counts['blue']}")


if __name__ == "__main__":
    main()