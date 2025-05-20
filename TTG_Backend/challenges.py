from game_logic import GameBoard, ComponentType, Marble

def create_default_board():
    board = GameBoard(8, 8)
    return board

def create_challenge_1_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 11)
    board.add_component(ComponentType.RAMP_LEFT, 6, 4)
    return board

def create_challenge_2_board():
    board = GameBoard(8,8)
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 7, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 9, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 10, 8)
    return board

def create_challenge_3_board():
    board = GameBoard(8,8)
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_LEFT, 9, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 10, 12)
    board.add_component(ComponentType.RAMP_RIGHT, 10, 10)
    board.add_component(ComponentType.RAMP_LEFT, 11, 11)
    board.add_component(ComponentType.RAMP_LEFT, 11, 9)
    return board

def create_challenge_4_board():
    board = GameBoard(8,8)
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 9, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 10, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 11, 5)
    board.add_component(ComponentType.RAMP_LEFT, 5, 3)
    board.add_component(ComponentType.RAMP_LEFT, 4, 4)
    board.add_component(ComponentType.RAMP_LEFT, 3, 5)
    return board

def create_challenge_5_board():
    board = GameBoard(8,8)
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.CROSSOVER, 7, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 12)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 6)
    board.add_component(ComponentType.RAMP_LEFT, 9, 11)
    board.add_component(ComponentType.RAMP_LEFT, 9, 9)
    board.add_component(ComponentType.RAMP_LEFT, 9, 7)
    return board

def create_challenge_6_board():
    board = GameBoard(8,8)
    board.set_number_of_marbles(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 12)
    board.add_component(ComponentType.RAMP_LEFT, 8, 12)
    board.add_component(ComponentType.RAMP_LEFT, 8, 10)
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)
    board.add_component(ComponentType.RAMP_LEFT, 8, 6)
    board.add_component(ComponentType.RAMP_LEFT, 8, 4)
    return board

def create_challenge_16_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 4)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.INTERCEPTOR, 4, 6)
    return board

def create_challenge_17_board():
    board = GameBoard(3, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_RIGHT, 5, 5)
    board.add_component(ComponentType.RAMP_LEFT, 6, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 4)
    board.add_component(ComponentType.BIT_LEFT, 9, 3)
    board.add_component(ComponentType.BIT_LEFT, 9, 5)
    board.add_component(ComponentType.INTERCEPTOR, 8, 6)
    return board

def create_challenge_18_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 7, 5)
    board.add_component(ComponentType.BIT_LEFT, 7, 7)
    board.add_component(ComponentType.INTERCEPTOR, 5, 9)
    board.add_component(ComponentType.INTERCEPTOR, 9, 9)
    return board

def create_challenge_19_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 7, 5)
    board.add_component(ComponentType.BIT_LEFT, 7, 7)
    board.add_component(ComponentType.INTERCEPTOR, 7, 13)
    return board

def create_challenge_20_board():
    board = GameBoard(0, 8)
    board.add_component(ComponentType.BIT_LEFT, 7, 5)
    board.add_component(ComponentType.BIT_LEFT, 7, 7)
    board.add_component(ComponentType.INTERCEPTOR, 7, 13)
    return board

def create_challenge_21_board():
    board = GameBoard(0, 15)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.BIT_LEFT, 5, 7)
    board.add_component(ComponentType.BIT_LEFT, 5, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 11)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 12)
    return board

def create_challenge_22_board():
    board = GameBoard(0, 15)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.BIT_LEFT, 5, 7)
    board.add_component(ComponentType.BIT_LEFT, 5, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 4, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 6)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 11)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 12)
    return board


CHALLENGES = {
    "default": {
        "id": "default",
        "board": create_default_board(),
        "red_marbles": 8,
        "blue_marbles": 8
    },
    "1": {
        "id":  "1",
        "board": create_challenge_1_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make all of the blue marbles (and only the blue marbles) reach the end.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 4"
    },
    "2": {
        "id":  "2",
        "board": create_challenge_2_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make all of the blue marbles (and only the blue marbles) reach the end.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 5"
    },
    "3": {
        "id":  "3",
        "board": create_challenge_3_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Release one blue marble and then all of the red marbles.",
        "expectedOutput": ['red', 'red', 'red','red', 'red', 'red', 'red', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 6"
    },
    "4": {
        "id":  "4",
        "board": create_challenge_4_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Release one red marble and then all of the blue marbles.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 13"
    },
    "5": {
        "id":  "5",
        "board": create_challenge_5_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make the pattern blue, red, blue, red, blue, red...",
        "expectedOutput": ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue'],
        "availableParts": "[ItemType.RampLeft]: 9"
    }
    ,
    "6": {
        "id":  "6",
        "board": create_challenge_6_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make the pattern blue, red, blue, red, blue, red...",
        "expectedOutput": ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue'],
        "availableParts": "[ItemType.RampLeft]: 2, [ItemType.Crossover]: 5"
    },
    "16": {
        "id":  "16",
        "board": create_challenge_16_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Let only 3 blue balls reach the bottom and catch the 4th ball in the interceptor.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 10"

    },
    "17": {
        "id":  "17",
        "board": create_challenge_17_board(),
        "red_marbles": 3,
        "blue_marbles": 3,
        "description": "Make the pattern blue, blue, blue, red, red, red",
        "expectedOutput": []
    },
    "18": {
        "id":  "18",
        "board": create_challenge_18_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "If the top bit AND the bottom bit start pointed to the right, intercept a blue ball. Otherwise, intercept a red ball.",
        "expectedOutput": []
    },
    "19": {
        "id":  "19",
        "board": create_challenge_19_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "If the top bit OR the bottom bit start pointed to the right, intercept a blue ball. Otherwise, intercept a red ball.",
        "expectedOutput": []
    },
    "20": {
        "id":  "20",
        "board": create_challenge_20_board(),
        "red_marbles": 0,
        "blue_marbles": 8,
        "description": "If the top bit OR the bottom bit start pointed to the right, intercept a blue ball. Otherwise, intercept a red ball.",
        "expectedOutput": []
    },
    "21": {
        "id":  "21",
        "board": create_challenge_21_board(),
        "red_marbles": 0,
        "blue_marbles": 15,
        "description": "Use register A to count the number of blue balls.",
        "expectedOutput": []
    },
    "22": {
        "id":  "22",
        "board": create_challenge_22_board(),
        "red_marbles": 0,
        "blue_marbles": 15,
        "description": "Make all of the blue marbles (and only the blue marbles) reach the end.",
        "expectedOutput": []
    },




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