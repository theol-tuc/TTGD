from game_state import GameStateSerializer
from game_logic import GameBoard, ComponentType

def test_serialization():
    # Create a test board
    board = GameBoard()
    
    # Add some test components
    board.add_component(ComponentType.GEAR, 7, 7)  # Add a gear in the middle
    board.add_component(ComponentType.BIT_LEFT, 6, 6)  # Add a bit
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)  # Add a ramp
    
    # Serialize the board
    json_state = GameStateSerializer.to_json(board)
    
    # Print the serialized state
    print("Serialized Game State:")
    print(json_state)
    
    # Deserialize back to dictionary
    state_dict = GameStateSerializer.from_json(json_state)
    
    # Verify the deserialized state
    assert state_dict["width"] == 15
    assert state_dict["height"] == 17
    assert len(state_dict["components"]) == 17  # height
    assert len(state_dict["components"][0]) == 15  # width
    
    # Check specific component positions
    gear_found = False
    bit_found = False
    ramp_found = False
    
    for y, row in enumerate(state_dict["components"]):
        for x, component in enumerate(row):
            if component["type"] == ComponentType.GEAR.value and x == 7 and y == 7:
                gear_found = True
            elif component["type"] == ComponentType.BIT_LEFT.value and x == 6 and y == 6:
                bit_found = True
            elif component["type"] == ComponentType.RAMP_LEFT.value and x == 8 and y == 8:
                ramp_found = True
    
    assert gear_found, "Gear not found in serialized state"
    assert bit_found, "Bit not found in serialized state"
    assert ramp_found, "Ramp not found in serialized state"
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_serialization() 