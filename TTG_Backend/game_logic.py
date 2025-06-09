# Core game mechanics and board representation for Turing Tumble
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional
import numpy as np

# Define component types using Enum for better structure and type safety
class ComponentType(Enum):
    EMPTY = 0
    RAMP_LEFT = 1
    RAMP_RIGHT = 2
    CROSSOVER = 3
    INTERCEPTOR = 4
    GEAR = 5
    BIT_LEFT = 6
    BIT_RIGHT = 7
    AND_GATE = 8
    OR_GATE = 9

# Define marble colors for the game
BLUE = "blue"
RED = "red"

# Represents a marble in the game with its properties
class Marble:
    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position
        self.direction = (0, 1)  # Initial direction is downward

# Base class for all board components with their properties and states
class Component:
    def __init__(self, type: ComponentType, position: Tuple[int, int]):
        self.type = type
        self.position = position
        self.state = 0  # For components that can store state (like bits)
        self.rotation = 0  # For components that can rotate (like gears)
        self.is_active = True
        self.connections = [False] * 8  # Connections to other components
        self.value = 0  # For components that store values
        self.is_output = False
        self.is_input = False

# Main game board class managing the state and interactions
class GameBoard:
    def __init__(self, width: int = 15, height: int = 17):
        self.width = width
        self.height = height
        # Initialize empty board with components
        self.board = [[Component(ComponentType.EMPTY, (x, y)) for x in range(width)] for y in range(height)]
        self.components: List[Component] = []
        self.marbles: List[Marble] = []
        self.outputs = {BLUE: [], RED: []}

    # Set a component at a specific position on the board
    def set_component(self, x: int, y: int, component_type: ComponentType) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            component = Component(component_type, (x, y))
            self.board[y][x] = component
            self.components.append(component)

    # Add a component at the specified position (alias for set_component)
    def add_component(self, component_type: ComponentType, x: int, y: int) -> None:
        self.set_component(x, y, component_type)

    # Add a marble at the specified x position
    def add_marble(self, color: str = BLUE, x: int = 7) -> None:
        if 0 <= x < self.width:
            marble = Marble(color, (x, 0))
            self.marbles.append(marble)

    # Drop a marble from the specified x position (alias for add_marble)
    def drop_marble(self, x: int, color: str = BLUE) -> None:
        self.add_marble(color, x)

    # Print the current state of the board for visualization
    def print_board(self) -> None:
        for y in range(self.height):
            row = []
            for x in range(self.width):
                component = self.board[y][x]
                if component.type == ComponentType.EMPTY:
                    row.append(".")
                elif component.type == ComponentType.RAMP_LEFT:
                    row.append("\\")
                elif component.type == ComponentType.RAMP_RIGHT:
                    row.append("/")
                elif component.type == ComponentType.CROSSOVER:
                    row.append("+")
                elif component.type == ComponentType.INTERCEPTOR:
                    row.append("X")
                elif component.type == ComponentType.GEAR:
                    row.append("G")
                elif component.type == ComponentType.BIT_LEFT:
                    row.append("L")
                elif component.type == ComponentType.BIT_RIGHT:
                    row.append("R")
                elif component.type == ComponentType.AND_GATE:
                    row.append("&")
                elif component.type == ComponentType.OR_GATE:
                    row.append("|")
                else:
                    row.append(" ")
            print("".join(row))

    # Get the component at a specific position
    def get_component_at(self, x: int, y: int) -> Optional[Component]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        return None

    # Check if a position is valid on the board
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    # Clear the board and reset all components
    def clear(self) -> None:
        self.board = [[Component(ComponentType.EMPTY, (x, y)) for x in range(self.width)] for y in range(self.height)]
        self.components = []
        self.marbles = []
        self.outputs = {BLUE: [], RED: []}

    # Update the game state based on marble movements and component interactions
    def update(self) -> None:
        for marble in self.marbles:
            if not marble.active:
                continue
            
            x, y = marble.position
            for comp in self.components:
                if comp.position == (x, y):
                    new_pos = comp.update(marble)
                    if new_pos:
                        marble.position = new_pos
                    break

    # Get the current board state as a numpy array for AI processing
    def get_board_state(self) -> np.ndarray:
        state = np.zeros((self.height, self.width), dtype=np.int32)
        for comp in self.components:
            x, y = comp.position
            state[y, x] = comp.type.value
        return state

    # Reset the board to its initial state
    def reset(self) -> None:
        self.marbles = []
        for comp in self.components:
            comp.state = 0

    # Set the number of marbles for each color
    def set_number_of_marbles(self, red, blue):
        self.red_marbles = red
        self.blue_marbles = blue
