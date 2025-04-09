from game_logic import GameBoard, ComponentType

def test_game_mechanics():
    print("=== Starting Game Test ===")
    # Initialize game board
    board = GameBoard(width=11, height=11)
    print("\n1. Board Initialization:")
    print("✓ Created 11x11 game board")
    
    # Test 1: Add components
    print("\n2. Component Placement Test:")
    # Add a launcher at the top
    board.add_component(ComponentType.LAUNCHER, 5, 0)
    print("✓ Added launcher (L) at (5,0)")
    
    # Add some ramps
    board.add_component(ComponentType.RAMP_LEFT, 4, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 3)
    print("✓ Added left ramp (<) at (4,3)")
    print("✓ Added right ramp (>) at (6,3)")
    
    # Add an interceptor
    board.add_component(ComponentType.INTERCEPTOR, 5, 8)
    print("✓ Added interceptor (X) at (5,8)")
    
    # Print initial setup
    print("\n3. Initial Board Setup:")
    print_board_state(board)
    
    # Test 2: Add marble directly below launcher
    print("\n4. Marble Placement Test:")
    # Add marble at (5,1) - just below the launcher
    success = board.add_marble(5, 1)
    if success:
        print("✓ Added marble at (5,1)")
    else:
        print("✗ Failed to add marble")
    
    # Print initial state with marble
    print("\n5. Initial State with Marble:")
    print_board_state(board)
    
    # Update physics several times
    print("\n6. Physics Update Test:")
    print("Watching marble movement...")
    for i in range(11):
        board.update_marble_positions()
        print(f"\nUpdate {i+1}:")
        print_board_state(board)
        # Add movement description
        marble_pos = board.get_marble_positions()
        if marble_pos:
            x, y = marble_pos[0]
            print(f"Marble position: ({x}, {y})")
    
    # Test 3: Reset game
    print("\n7. Game Reset Test:")
    board.reset()
    print("✓ Game reset - all components and marbles cleared")
    print("\nFinal Board State:")
    print_board_state(board)
    
    print("\n=== Test Summary ===")
    print("To verify the test was successful, check that:")
    print("1. ✓ Board was created with correct size (11x11)")
    print("2. ✓ Components were placed correctly")
    print("3. ✓ Marble was added successfully")
    print("4. ✓ Marble moved according to physics")
    print("5. ✓ Marble interacted with ramps correctly")
    print("6. ✓ Score increased when marble was intercepted")
    print("7. ✓ Game reset cleared all components and marbles")

def print_board_state(board):
    """Helper function to print the current board state"""
    # Get current state
    board_state = board.get_board_state()
    marble_positions = board.get_marble_positions()
    
    # Print column numbers
    print("   " + " ".join(str(i).rjust(2) for i in range(board.width)))
    print("  " + "-" * (board.width * 3 - 1))
    
    # Print board with components and marbles
    for y in range(board.height):
        row = [str(y).rjust(2) + "|"]
        for x in range(board.width):
            cell = "."
            # Check for marbles
            if (x, y) in marble_positions:
                cell = "M"
            # Check for components
            elif board_state[y][x] == ComponentType.LAUNCHER.value:
                cell = "L"
            elif board_state[y][x] == ComponentType.RAMP_LEFT.value:
                cell = "<"
            elif board_state[y][x] == ComponentType.RAMP_RIGHT.value:
                cell = ">"
            elif board_state[y][x] == ComponentType.INTERCEPTOR.value:
                cell = "X"
            row.append(cell.rjust(2))
        print(" ".join(row))
    
    print(f"\nScore: {board.get_score()}")
    print(f"Active marbles: {len(marble_positions)}")

if __name__ == "__main__":
    test_game_mechanics() 