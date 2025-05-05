# Turing Tumble Implementation Guide

## Game State Serialization (Task #91) and LLM Board Encoding (Task #93)

### 1. Game State Serialization

The `GameStateSerializer` class provides methods to convert the game state to and from JSON format.

#### Basic Usage:
```python
from game_state import GameStateSerializer
from game_logic import GameBoard

# Create a game board
board = GameBoard()

# Serialize to JSON
json_state = GameStateSerializer.to_json(board)

# Deserialize back to board
reconstructed_board = GameStateSerializer.from_json_to_board(json_state)
```

#### Serialized State Structure:
```json
{
    "width": 15,
    "height": 17,
    "components": [
        {
            "type": "component_type",
            "x": 0,
            "y": 0,
            "is_occupied": false,
            "gear_rotation": 0,
            "gear_bit_state": 0
        }
    ],
    "marbles": [
        {
            "color": "red",
            "x": 0,
            "y": 0,
            "direction": "down",
            "is_moving": true
        }
    ],
    "active_launcher": "right",
    "red_marbles": 8,
    "blue_marbles": 8
}
```

### 2. LLM Board Encoding

The `BoardEncoder` class converts the game state into a format understandable by Language Learning Models.

#### Basic Usage:
```python
from board_encoder import BoardEncoder
from game_logic import GameBoard

# Create a game board
board = GameBoard()

# Encode for LLM
encoded_state = BoardEncoder.encode_board(board)

# Get game rules
rules = BoardEncoder.encode_game_rules()
```

#### Encoded State Structure:
```
Turing Tumble Game State:

Board Layout:
[Visual representation of the board]

Active Components:
- gear at position (7, 7)
- bit_left at position (6, 6)
- ramp_left at position (8, 8)

Marble States:
- Red marble at (3, 3) moving down
- Blue marble at (4, 4) moving left

Game Status:
- Active Launcher: right
- Red Marbles: 2
- Blue Marbles: 1

Possible Actions:
1. Launch marble from right launcher
2. Move gear at (7, 7)
3. Flip bit at (6, 6)
```

### 3. Integration with AI Tasks

#### For Hybrid Neuro-Symbolic Agent (Task #99):
- Use `GameStateSerializer` to save and load game states
- Use `BoardEncoder` to provide symbolic representation for the agent
- Example:
```python
# Get symbolic representation for agent
encoded_state = BoardEncoder.encode_board(board)
# Agent can now understand the game state
```

#### For AI Model Implementation (Task #84):
- Use serialized state for training data
- Use encoded state for model input
- Example:
```python
# Prepare training data
json_state = GameStateSerializer.to_json(board)
# Prepare model input
encoded_state = BoardEncoder.encode_board(board)
```

#### For Vision-Language Model (Task #100):
- Use encoded state for language understanding
- Combine with visual representation
- Example:
```python
# Get language representation
encoded_state = BoardEncoder.encode_board(board)
# Combine with visual data
```

### 4. Testing

Run the tests to verify the implementations:
```bash
# Test serialization
python test_game_state.py

# Test LLM encoding
python test_board_encoder.py

# Test combined functionality
python test_combined.py
```

### 5. Future Extensions

1. Add more component types
2. Enhance encoding for specific AI tasks
3. Add more game state properties
4. Implement additional serialization formats

### 6. Common Issues and Solutions

1. **Serialization Errors**
   - Check component types
   - Verify board dimensions
   - Ensure all required properties are present

2. **Encoding Issues**
   - Verify component positions
   - Check marble states
   - Ensure proper formatting

### 7. Support

For questions or issues:
1. Check the test files for examples
2. Review the implementation guide
3. Contact the implementation team 