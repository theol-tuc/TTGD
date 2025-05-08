from game_logic import GameBoard, ComponentType, Marble

def create_default_board():
    board = GameBoard()
    board.set_number_of_marbles(8, 8)
    return board

def create_challenge_1_board():
    board = GameBoard()
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 11)
    board.add_component(ComponentType.RAMP_LEFT, 6, 4)
    return board

CHALLENGES = {
    "default": {
        "id": "default",
        "board": create_default_board()
    },
    "1": {
        "id":  "1",
        "board": create_challenge_1_board()
    }
}

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