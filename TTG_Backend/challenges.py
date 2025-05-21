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

def create_challenge_7_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.CROSSOVER,5,5)
    board.add_component(ComponentType.CROSSOVER,7,5)
    board.add_component(ComponentType.CROSSOVER,3,7)
    board.add_component(ComponentType.CROSSOVER,6,8)
    board.add_component(ComponentType.CROSSOVER,5,11)
    board.add_component(ComponentType.CROSSOVER,4,10)
    return board

def create_challenge_8_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.RAMP_RIGHT,5,3)
    board.add_component(ComponentType.RAMP_RIGHT,6,4)
    board.add_component(ComponentType.RAMP_LEFT,9,3)
    board.add_component(ComponentType.RAMP_LEFT,8,4)
    board.add_component(ComponentType.BIT_RIGHT,7,5)
    return board

def create_challenge_9_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.BIT_RIGHT,5,3)
    board.add_component(ComponentType.RAMP_RIGHT,6,4)
    board.add_component(ComponentType.RAMP_LEFT,9,3)
    board.add_component(ComponentType.RAMP_LEFT,8,4)
    board.add_component(ComponentType.CROSSOVER,7,5)
    return board

def create_challenge_10_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.BIT_RIGHT,5,3)
    board.add_component(ComponentType.BIT_LEFT,9,3)
    board.add_component(ComponentType.CROSSOVER,7,5)
    return board

def create_challenge_11_board():
    board = GameBoard(0,2)
    board.add_component(ComponentType.BIT_RIGHT,7,5)
    board.add_component(ComponentType.BIT_LEFT,3,9)
    board.add_component(ComponentType.BIT_LEFT,5,9)
    board.add_component(ComponentType.BIT_LEFT,7,9)
    board.add_component(ComponentType.BIT_LEFT,9,9)
    board.add_component(ComponentType.BIT_LEFT,11,9)
    return board

def create_challenge_12_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.RAMP_RIGHT,5,3)
    board.add_component(ComponentType.RAMP_RIGHT,6,4)
    board.add_component(ComponentType.BIT_RIGHT,7,5)
    board.add_component(ComponentType.RAMP_LEFT,9,9)
    board.add_component(ComponentType.RAMP_LEFT,8,10)
    board.add_component(ComponentType.INTERCEPTOR, 7, 11)
    return board

def create_challenge_13_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.RAMP_RIGHT,5,3)
    board.add_component(ComponentType.RAMP_RIGHT,6,4)
    board.add_component(ComponentType.BIT_RIGHT,7,5)
    board.add_component(ComponentType.RAMP_RIGHT,8,6)
    board.add_component(ComponentType.RAMP_RIGHT,9,7)
    board.add_component(ComponentType.RAMP_LEFT,10,8)
    board.add_component(ComponentType.RAMP_LEFT,9,9)
    board.add_component(ComponentType.RAMP_LEFT,8,10)
    board.add_component(ComponentType.INTERCEPTOR, 7, 11)
    return board

def create_challenge_14_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.BIT_RIGHT,7,5)
    board.add_component(ComponentType.INTERCEPTOR, 7, 11)
    return board

def create_challenge_15_board():
    board = GameBoard(8,8)
    board.add_component(ComponentType.BIT_RIGHT,5,3)
    board.add_component(ComponentType.RAMP_RIGHT,6,4)
    board.add_component(ComponentType.RAMP_LEFT,9,3)
    board.add_component(ComponentType.RAMP_LEFT,8,4)
    board.add_component(ComponentType.INTERCEPTOR,7,5)
    board.add_component(ComponentType.BIT_RIGHT, 7, 11)
    return board

def create_challenge_16_board():
    board = GameBoard(8,8)
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

def create_challenge_23_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.BIT_LEFT, 5, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 3, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 3, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 3, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 3, 11)
    board.add_component(ComponentType.RAMP_LEFT, 4, 4)
    board.add_component(ComponentType.RAMP_LEFT, 4, 6)
    board.add_component(ComponentType.RAMP_LEFT, 4, 8)
    board.add_component(ComponentType.RAMP_LEFT, 4, 10)
    board.add_component(ComponentType.RAMP_LEFT, 4, 12)
    board.add_component(ComponentType.RAMP_LEFT, 6, 4)
    board.add_component(ComponentType.RAMP_LEFT, 6, 6)
    board.add_component(ComponentType.INTERCEPTOR, 6, 8)
    return board

def create_challenge_24_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.BIT_LEFT, 5, 7)
    board.add_component(ComponentType.BIT_LEFT, 5, 9)
    return board

def create_challenge_25_board():
    board = GameBoard(8, 8)
    return board

def create_challenge_26_board():
    board = GameBoard(10, 10)
    board.add_component(ComponentType.BIT_LEFT, 9, 3)
    board.add_component(ComponentType.INTERCEPTOR, 10, 4)
    return board

def create_challenge_27_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 4, 4)
    board.add_component(ComponentType.BIT_LEFT, 4, 6)
    board.add_component(ComponentType.BIT_LEFT, 4, 8)
    board.add_component(ComponentType.BIT_LEFT, 4, 10)
    board.add_component(ComponentType.BIT_LEFT, 7, 5)
    board.add_component(ComponentType.BIT_LEFT, 7, 7)
    board.add_component(ComponentType.BIT_LEFT, 7, 9)
    board.add_component(ComponentType.BIT_LEFT, 7, 11)
    board.add_component(ComponentType.BIT_LEFT, 10, 4)
    return board

def create_challenge_28_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 3)
    board.add_component(ComponentType.RAMP_RIGHT, 6, 4)
    board.add_component(ComponentType.RAMP_LEFT, 9, 3)
    board.add_component(ComponentType.RAMP_LEFT, 8, 4)
    board.add_component(ComponentType.GEAR_BIT_RIGHT, 7, 5)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 7)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 9)
    board.add_component(ComponentType.RAMP_RIGHT, 5, 11)
    board.add_component(ComponentType.RAMP_LEFT, 6, 8)
    board.add_component(ComponentType.RAMP_LEFT, 6, 10)
    board.add_component(ComponentType.RAMP_LEFT, 6, 12)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 8)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 10)
    board.add_component(ComponentType.RAMP_RIGHT, 8, 12)
    board.add_component(ComponentType.RAMP_LEFT, 9, 7)
    board.add_component(ComponentType.RAMP_LEFT, 9, 9)
    board.add_component(ComponentType.RAMP_LEFT, 9, 11)
    return board

def create_challenge_29_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.GEAR_BIT_LEFT, 5, 3)
    return board

def create_challenge_30_board():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.BIT_LEFT, 5, 3)
    board.add_component(ComponentType.BIT_LEFT, 5, 5)
    board.add_component(ComponentType.BIT_LEFT, 5, 7)
    board.add_component(ComponentType.GEAR_BIT_LEFT, 4, 7)

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
    "7": {
        "id":  "7",
        "board": create_challenge_7_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Create a path for the blue marbles to reach the output with only 6 ramps.",
        "expectedOutput": ['blue', 'blue', 'blue','blue', 'blue', 'blue','blue','blue'],
        "availableParts": "[ItemType.RampLeft]: 6"
    },
    "8": {
        "id":  "8",
        "board": create_challenge_8_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make the pattern blue, red, blue, red, blue, red...",
        "expectedOutput": ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue'],
        "availableParts": "[ItemType.RampLeft]: 14"
    },
    "9": {
        "id":  "9",
        "board": create_challenge_9_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make the pattern blue, blue, red, blue, blue, red...",
        "expectedOutput": ['red','blue','blue', 'red','blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 18"
    },
    "10": {
        "id":  "10",
        "board": create_challenge_10_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Make the pattern blue, blue, red, red, blue, blue, red, red...",
        "expectedOutput": ['red','red','blue','blue', 'red','red','blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 22"
    },
    "11": {
        "id":  "11",
        "board": create_challenge_11_board(),
        "red_marbles": 0,
        "blue_marbles": 2,
        "description": "Flip the bits with the coordinates (3,9) and (11,9) to the right.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 15"
    },
    "12": {
        "id":  "12",
        "board": create_challenge_12_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Intercept a blue marble.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 3"
    },
    "13": {
        "id":  "13",
        "board": create_challenge_13_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Intercept a red marble. Start with trigger Left",
        "expectedOutput": ['blue'],
        "availableParts": "[ItemType.RampLeft]: 12"
    },
    "14": {
        "id":  "14",
        "board": create_challenge_14_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "If the challenge starts with the bit pointing to the left, intercept a blue marble. Otherwise, intercept a red marble.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 20"
    },
    "15": {
        "id":  "15",
        "board": create_challenge_15_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "If the bit with the coordinates (7,11) starts to the left, intercept a blue marble. Otherwise, intercept a red marble.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 11, [ItemType.Crossover]: 2"
    },
    "16": {
        "id":  "16",
        "board": create_challenge_16_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "description": "Let only 3 blue marbles reach the bottom and catch the 4th marble in the interceptor.",
        "expectedOutput": ['blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 10"

    },
    "17": {
        "id":  "17",
        "board": create_challenge_17_board(),
        "red_marbles": 3,
        "blue_marbles": 3,
        "Description": "Make the pattern blue, blue, blue, red, red, red",
        "expectedOutput": ['blue', 'blue', 'blue', 'red', 'red', 'red'],
        "availableParts": "[ItemType.RampLeft]: 999"
    },
    "18": {
        "id":  "18",
        "board": create_challenge_18_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "If the top bit AND the bottom bit start pointed to the right, put a marble in the left interceptor. Else, put a marble in the right interceptor.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 7"
    },
    "19": {
        "id":  "19",
        "board": create_challenge_19_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "If the top bit AND the bottom bit start pointed to the right, intercept a blue marble. Otherwise, intercept a red marble.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2"
    },
    "20": {
        "id":  "20",
        "board": create_challenge_20_board(),
        "red_marbles": 0,
        "blue_marbles": 8,
        "Description": "If the top bit OR the bottom bit start pointed to the right, intercept a blue marble. Otherwise, intercept a red marble.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2"
    },
    "21": {
        "id":  "21",
        "board": create_challenge_21_board(),
        "red_marbles": 0,
        "blue_marbles": 15,
        "Description": "On a Turing Tumble board, each bit component has two states—left and right—which represent binary 0 and 1. When you align multiple bits vertically and let marbles flow through them from top to bottom, the structure behaves like a binary register. You can simulate binary increment and decrement using vertical bit registers on a Turing Tumble board. Each operation involves flipping bits from the LSB upward, with carry for incrementing and borrow for decrementing, just like in standard binary arithmetic. Use the marble’s path and bit flipping behavior to implement these transformations physically. Use the register formed by the bits on the board to count the number of blue marbles.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 5"
    },
    "22": {
        "id":  "22",
        "board": create_challenge_22_board(),
        "red_marbles": 0,
        "blue_marbles": 15,
        "Description": "On a Turing Tumble board, each bit component has two states—left and right—which represent binary 0 and 1. When you align multiple bits vertically and let marbles flow through them from top to bottom, the structure behaves like a binary register. You can simulate binary increment and decrement using vertical bit registers on a Turing Tumble board. Each operation involves flipping bits from the LSB upward, with carry for incrementing and borrow for decrementing, just like in standard binary arithmetic. Use the marble’s path and bit flipping behavior to implement these transformations physically. The register formed by the bits on the board starts at the value 15. Subtract the number of blue marbles from the register.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 4"
    },
    "23": {
        "id":  "23",
        "board": create_challenge_23_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Let exactly 4 blue marbles reach the end. (Intercept the 5th.)",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue'],
        "availableParts": "none"
    },
    "24": {
        "id":  "24",
        "board": create_challenge_24_board(),
        "red_marbles": 12,
        "blue_marbles": 12,
        "Description": " Let exactly 9 blue marbles reach the end. (Intercept the 10th.)",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 14, [ItemType.Intercept]: 1"
    },
    "25": {
        "id":  "25",
        "board": create_challenge_25_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Generate the required pattern.",
        "expectedOutput": ['red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Intercept]: 1, [ItemType.BitLeft]: 5"
    },
    "26": {
        "id":  "26",
        "board": create_challenge_26_board(),
        "red_marbles": 10,
        "blue_marbles": 10,
        "Description": "Generate the required pattern.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2, [ItemType.BitLeft]: 2"
    },
    "27": {
        "id":  "27",
        "board": create_challenge_27_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Reverse the direction of each of the 9 starting bits, regardless of the direction they point to start.",
        "expectedOutput": [],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Intercept]: 1, [ItemType.BitLeft]: 1"
    },
    "28": {
        "id":  "28",
        "board": create_challenge_28_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Generate the required pattern.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2, [ItemType.BitLeft]: 2"
    },
    "29": {
        "id":  "29",
        "board": create_challenge_29_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Generate the required pattern.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2, [ItemType.BitLeft]: 2"
    },
    "30": {
        "id":  "30",
        "board": create_challenge_30_board(),
        "red_marbles": 8,
        "blue_marbles": 8,
        "Description": "Generate the required pattern.",
        "expectedOutput": ['blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue'],
        "availableParts": "[ItemType.RampLeft]: 999, [ItemType.Crossover]: 2, [ItemType.BitLeft]: 2"
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