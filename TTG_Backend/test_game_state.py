from game_state import GameStateSerializer
from game_logic import GameBoard, ComponentType

def test_serialization_and_deserialization():
    # Create a test board
    board = GameBoard()
    
    # Add some test components
    board.add_component(ComponentType.GEAR, 7, 7)  # Add a gear in the middle
    board.add_component(ComponentType.BIT_LEFT, 6, 6)  # Add a bit
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)  # Add a ramp
    
    # Set some board properties
    board.active_launcher = "right"
    board.red_marbles = 3
    board.blue_marbles = 2
    
    # Serialize the board
    json_state = GameStateSerializer.to_json(board)
    
    # Deserialize back to a new board
    reconstructed_board = GameStateSerializer.from_json_to_board(json_state)
    
    # Verify the reconstructed board
    assert reconstructed_board.width == 15
    assert reconstructed_board.height == 17
    assert reconstructed_board.active_launcher == "right"
    assert reconstructed_board.red_marbles == 3
    assert reconstructed_board.blue_marbles == 2
    
    # Check specific component positions
    gear_found = False
    bit_found = False
    ramp_found = False
    
    for y, row in enumerate(reconstructed_board.components):
        for x, component in enumerate(row):
            if component.type == ComponentType.GEAR and x == 7 and y == 7:
                gear_found = True
            elif component.type == ComponentType.BIT_LEFT and x == 6 and y == 6:
                bit_found = True
            elif component.type == ComponentType.RAMP_LEFT and x == 8 and y == 8:
                ramp_found = True
    
    assert gear_found, "Gear not found in reconstructed board"
    assert bit_found, "Bit not found in reconstructed board"
    assert ramp_found, "Ramp not found in reconstructed board"
    
    print("\nAll serialization and deserialization tests passed!")

if __name__ == "__main__":
    test_serialization_and_deserialization() 