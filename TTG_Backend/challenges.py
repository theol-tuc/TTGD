from TTG_Backend.game_logic import GameBoard, ComponentType, Marble
from TTG_Backend.graph_parser import update_challenges_with_gv
from typing import Dict, Any

def create_default_board():
    board = GameBoard()
    board.set_number_of_marbles(8, 8)
    return board

def create_challenge_1_board() -> GameBoard:
    """Create a simple challenge board"""
    board = GameBoard()
    
    # Add some test components
    board.set_component(7, 5, ComponentType.RAMP_LEFT)
    board.set_component(7, 7, ComponentType.RAMP_RIGHT)
    board.set_component(7, 3, ComponentType.CROSSOVER)
    board.set_component(6, 4, ComponentType.INTERCEPTOR)
    
    return board

def create_challenge_2_board() -> GameBoard:
    """Create a more complex challenge board"""
    board = GameBoard()
    
    # Add components for a more complex puzzle
    board.set_component(7, 3, ComponentType.GEAR)
    board.set_component(8, 4, ComponentType.BIT_LEFT)
    board.set_component(6, 4, ComponentType.BIT_RIGHT)
    board.set_component(7, 5, ComponentType.AND_GATE)
    board.set_component(7, 7, ComponentType.OR_GATE)
    
    return board

def create_challenge_3_board():
    """Pattern matching challenge"""
    board = GameBoard()
    board.set_number_of_marbles(6, 6)
    # Create a pattern of ramps and crossovers
    board.add_component(ComponentType.RAMP_RIGHT, 4, 3)
    board.add_component(ComponentType.CROSSOVER, 4, 5)
    board.add_component(ComponentType.RAMP_LEFT, 4, 7)
    board.add_component(ComponentType.INTERCEPTOR, 5, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 6)
    return board

def create_challenge_4_board():
    """Complex graph challenge with multiple paths"""
    board = GameBoard()
    board.set_number_of_marbles(10, 10)
    # Create a complex network of components
    # Main path
    board.add_component(ComponentType.RAMP_RIGHT, 4, 3)
    board.add_component(ComponentType.CROSSOVER, 4, 5)
    board.add_component(ComponentType.RAMP_LEFT, 4, 7)
    # Branching paths
    board.add_component(ComponentType.RAMP_RIGHT, 5, 4)
    board.add_component(ComponentType.GEAR, 5, 6)
    board.add_component(ComponentType.RAMP_LEFT, 5, 8)
    # Additional components
    board.add_component(ComponentType.INTERCEPTOR, 6, 5)
    board.add_component(ComponentType.CROSSOVER, 6, 7)
    return board

def create_challenge_5_board():
    """Logic gate challenge"""
    board = GameBoard()
    board.set_number_of_marbles(8, 8)
    # Create AND gate
    board.add_component(ComponentType.RAMP_RIGHT, 4, 3)
    board.add_component(ComponentType.RAMP_LEFT, 4, 5)
    board.add_component(ComponentType.GEAR, 5, 4)
    # Create OR gate
    board.add_component(ComponentType.RAMP_RIGHT, 6, 3)
    board.add_component(ComponentType.RAMP_LEFT, 6, 5)
    board.add_component(ComponentType.CROSSOVER, 7, 4)
    return board

# Basic challenges
BASIC_CHALLENGES = {
    "default": {
        "id": "default",
        "board": create_default_board(),
        "description": "Default empty board"
    },
    "1": {
        "id": "1",
        "board": create_challenge_1_board(),
        "description": "Simple ramp pattern challenge"
    },
    "2": {
        "id": "2",
        "board": create_challenge_2_board(),
        "description": "Binary counter challenge"
    },
    "3": {
        "id": "3",
        "board": create_challenge_3_board(),
        "description": "Pattern matching challenge"
    },
    "4": {
        "id": "4",
        "board": create_challenge_4_board(),
        "description": "Complex graph challenge with multiple paths"
    },
    "5": {
        "id": "5",
        "board": create_challenge_5_board(),
        "description": "Logic gate challenge"
    }
}

# Load GraphViz-based challenges
try:
    GV_CHALLENGES = update_challenges_with_gv()
except Exception as e:
    print(f"Warning: Failed to load GraphViz challenges: {str(e)}")
    GV_CHALLENGES = {}

# Combine all challenges
CHALLENGES = {**BASIC_CHALLENGES, **GV_CHALLENGES}

def serialize_challenge(board: GameBoard):
    """Convert GameBoard to a JSON-serializable format."""
    components = []
    for row in board.components:
        component_row = []
        for component in row:
            component_row.append({
                "type": component.type.value,
                "is_occupied": component.is_occupied
            })
        components.append(component_row)
    return components

# Initialize challenges
CHALLENGES["challenge1"] = {
    "name": "Simple Ramp Challenge",
    "description": "Create a path for the blue marble using ramps",
    "board": create_challenge_1_board(),
    "objective": "Guide the blue marble to the bottom center"
}

CHALLENGES["challenge2"] = {
    "name": "Logic Gate Challenge",
    "description": "Use logic gates to control marble paths",
    "board": create_challenge_2_board(),
    "objective": "Create a circuit that alternates between two outputs"
}

def get_challenge(challenge_id: str) -> Dict[str, Any]:
    """Get a challenge by its ID"""
    return CHALLENGES.get(challenge_id, {})

def list_challenges() -> Dict[str, Dict[str, Any]]:
    """List all available challenges"""
    return CHALLENGES