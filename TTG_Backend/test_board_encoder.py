from board_encoder import BoardEncoder
from game_logic import GameBoard, ComponentType

def test_board_encoding():
    # Create a test board
    board = GameBoard()
    
    # Add test components
    board.add_component(ComponentType.GEAR, 7, 7)
    board.add_component(ComponentType.BIT_LEFT, 6, 6)
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)
    
    # Set board properties
    board.active_launcher = "right"
    board.red_marbles = 2
    board.blue_marbles = 1
    
    # Encode the board
    encoded_state = BoardEncoder.encode_board(board)
    
    # Verify the encoded state contains all necessary information
    assert "Turing Tumble Game State" in encoded_state
    assert "Board Layout" in encoded_state
    assert "Active Components" in encoded_state
    assert "Marble States" in encoded_state
    assert "Game Status" in encoded_state
    assert "Possible Actions" in encoded_state
    
    # Verify component encoding
    assert "gear at position (7, 7)" in encoded_state
    assert "bit_left at position (6, 6)" in encoded_state
    assert "ramp_left at position (8, 8)" in encoded_state
    
    # Verify game status
    assert "Active Launcher: right" in encoded_state
    assert "Red Marbles: 2" in encoded_state
    assert "Blue Marbles: 1" in encoded_state
    
    # Test game rules encoding
    rules = BoardEncoder.encode_game_rules()
    assert "Turing Tumble Game Rules" in rules
    assert "Board Layout" in rules
    assert "Components" in rules
    assert "Marbles" in rules
    assert "Winning Conditions" in rules
    
    print("\nAll board encoding tests passed!")

if __name__ == "__main__":
    test_board_encoding() 