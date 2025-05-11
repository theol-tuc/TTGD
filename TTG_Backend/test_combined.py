from game_state import GameStateSerializer
from board_encoder import BoardEncoder
from game_logic import GameBoard, ComponentType

def test_serialization_and_encoding():
    print("Starting combined test of serialization and LLM encoding...")
    
    # Create a test board with various components
    board = GameBoard()
    
    # Add different types of components
    print("\n1. Setting up test board...")
    board.add_component(ComponentType.GEAR, 7, 7)
    board.add_component(ComponentType.BIT_LEFT, 6, 6)
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)
    board.add_component(ComponentType.CROSSOVER, 7, 6)
    board.add_component(ComponentType.INTERCEPTOR, 7, 8)
    
    # Set board properties
    board.active_launcher = "right"
    board.red_marbles = 2
    board.blue_marbles = 1
    
    # Test 1: Serialization
    print("\n2. Testing serialization...")
    json_state = GameStateSerializer.to_json(board)
    print("✓ Board serialized to JSON")
    
    # Test 2: Deserialization
    print("\n3. Testing deserialization...")
    reconstructed_board = GameStateSerializer.from_json_to_board(json_state)
    print("✓ Board reconstructed from JSON")
    
    # Verify reconstructed board
    assert reconstructed_board.width == 15
    assert reconstructed_board.height == 17
    assert reconstructed_board.active_launcher == "right"
    assert reconstructed_board.red_marbles == 2
    assert reconstructed_board.blue_marbles == 1
    print("✓ Board properties verified")
    
    # Test 3: LLM Encoding
    print("\n4. Testing LLM encoding...")
    encoded_state = BoardEncoder.encode_board(board)
    print("✓ Board encoded for LLM")
    
    # Verify encoded state contains all necessary information
    assert "Turing Tumble Game State" in encoded_state
    assert "Board Layout" in encoded_state
    assert "Active Components" in encoded_state
    assert "Game Status" in encoded_state
    print("✓ Encoded state structure verified")
    
    # Test 4: Component Verification
    print("\n5. Verifying components...")
    # Check if all components are present in both formats
    components_to_check = [
        (ComponentType.GEAR, 7, 7),
        (ComponentType.BIT_LEFT, 6, 6),
        (ComponentType.RAMP_LEFT, 8, 8),
        (ComponentType.CROSSOVER, 7, 6),
        (ComponentType.INTERCEPTOR, 7, 8)
    ]
    
    for comp_type, x, y in components_to_check:
        # Check in reconstructed board
        assert reconstructed_board.components[y][x].type == comp_type, f"Component {comp_type.value} not found at ({x}, {y}) in reconstructed board"
        # Check in encoded state
        assert f"{comp_type.value} at position ({x}, {y})" in encoded_state, f"Component {comp_type.value} not found in encoded state"
    
    print("✓ All components verified in both formats")
    
    # Test 5: Print sample outputs
    print("\n6. Sample Outputs:")
    print("\nJSON State (first 200 characters):")
    print(json_state[:200] + "...")
    
    print("\nLLM Encoded State (first 200 characters):")
    print(encoded_state[:200] + "...")
    
    print("\nAll tests passed successfully!")
    print("\nSummary:")
    print("- Serialization: ✓")
    print("- Deserialization: ✓")
    print("- LLM Encoding: ✓")
    print("- Component Verification: ✓")
    print("- State Preservation: ✓")

if __name__ == "__main__":
    test_serialization_and_encoding() 