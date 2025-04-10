from typing import List, Tuple, Optional, Dict
import numpy as np
from enum import Enum


class ComponentType(Enum):
    EMPTY = "empty"
    RAMP_LEFT = "ramp_left"
    RAMP_RIGHT = "ramp_right"
    CROSSOVER = "crossover"
    INTERCEPTOR = "interceptor"
    LAUNCHER = "launcher"
    BIT_LEFT = "bit_left"
    BIT_RIGHT = "bit_right"
    BORDER_VERTICAL = "border_vertical"
    BORDER_HORIZONTAL = "border_horizontal"
    BORDER_DIAGONAL_LEFT = "border_diagonal_left"
    BORDER_DIAGONAL_RIGHT = "border_diagonal_right"
    CORNER_LEFT = "corner_left"
    CORNER_RIGHT = "corner_right"
    INVALID = "invalid"
    GRAY_SPACE = "gray_space"
    LEVER_BLUE = "lever_blue"
    LEVER_RED = "lever_red"


class Component:
    def __init__(self, type: ComponentType, x: int, y: int):
        self.type = type
        self.x = x
        self.y = y
        self.is_occupied = False


class Marble:
    def __init__(self, color: str, x: int, y: int):
        self.color = color
        self.x = x
        self.y = y
        self.direction = "down"
        self.is_moving = True


class GameBoard:
    def __init__(self, width: int = 15, height: int = 17):
        self.width = width
        self.height = height
        self.components: List[List[Component]] = []
        self.marbles: List[Marble] = []
        self.active_launcher = "left"
        self.red_marbles = 0
        self.blue_marbles = 0
        self.initialize_board()

    def initialize_board(self) -> None:
        """Initialize the board with empty components"""
        self.components = [[Component(ComponentType.EMPTY, x, y)
                            for x in range(self.width)]
                           for y in range(self.height)]

        # Set up borders and invalid spaces
        self.setup_board_structure()

    def setup_board_structure(self) -> None:
        """Set up the board structure with borders and invalid spaces"""
        # Set vertical borders
        for y in range(self.height):
            self.components[y][0].type = ComponentType.BORDER_VERTICAL
            self.components[y][self.width - 1].type = ComponentType.BORDER_VERTICAL

        # Set horizontal border (last row)
        for x in range(self.width):
            self.components[self.height - 1][x].type = ComponentType.BORDER_HORIZONTAL

        # Set up the diamond pattern
        self.setup_diamond_pattern()

        # Add levers at the bottom
        self.components[self.height - 3][6].type = ComponentType.LEVER_BLUE  # Left lever for blue marbles
        self.components[self.height - 3][8].type = ComponentType.LEVER_RED  # Right lever for red marbles

        # Add corners
        self.components[self.height - 1][0].type = ComponentType.CORNER_LEFT
        self.components[self.height - 1][self.width - 1].type = ComponentType.CORNER_RIGHT

        # Add launchers at the top
        self.components[0][3].type = ComponentType.LAUNCHER  # Left launcher for blue marbles
        self.components[0][11].type = ComponentType.LAUNCHER  # Right launcher for red marbles

    def setup_diamond_pattern(self) -> None:
        """Set up the diamond pattern of invalid spaces"""
        # Row 1 (index 0)
        for x in range(1, self.width - 1):
            if x == 1 or (3 <= x <= 11) or x == 13:
                self.components[0][x].type = ComponentType.INVALID
            elif x == 2:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 12:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 2 (index 1)
        for x in range(1, self.width - 1):
            if x in [1, 2] or (4 <= x <= 10) or x in [12, 13]:
                self.components[1][x].type = ComponentType.INVALID
            elif x == 3:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 11:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 3 (index 2)
        for x in range(1, self.width - 1):
            if x in [1, 2, 3] or (5 <= x <= 9) or x in [11, 12, 13]:
                self.components[2][x].type = ComponentType.INVALID
            elif x == 4:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 10:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Middle rows
        for y in range(3, self.height - 3):
            self.components[y][1].type = ComponentType.INVALID
            self.components[y][self.width - 2].type = ComponentType.INVALID

        # Bottom rows
        for y in range(self.height - 3, self.height - 1):
            for x in range(1, self.width - 1):
                if (x <= 6) or (x >= 8):
                    self.components[y][x].type = ComponentType.INVALID

    def add_component(self, type: ComponentType, x: int, y: int) -> None:
        """Add a component to the board"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.components[y][x] = Component(type, x, y)

    def set_active_launcher(self, launcher: str) -> None:
        """Set the active launcher (left or right)"""
        self.active_launcher = launcher

    def launch_marble(self, color: str) -> None:
        """Launch a marble from the active launcher"""
        if self.active_launcher == "left":
            x = 3  # Left launcher position
            # Left side always uses blue marbles
            color = "blue"
        else:
            x = 11  # Right launcher position
            # Right side always uses red marbles
            color = "red"
        y = 0  # Top row

        # Check if position is valid
        if 0 <= x < self.width and 0 <= y < self.height:
            if not self.check_collision(x, y):
                self.marbles.append(Marble(color, x, y))
                self.components[y][x].is_occupied = True

    def check_collision(self, x: int, y: int) -> bool:
        """Check if a position is occupied"""
        return self.components[y][x].is_occupied

    def update_marble_positions(self) -> None:
        """Update all marble positions based on components and physics"""
        marbles_to_remove = []

        for marble in self.marbles:
            if not marble.is_moving:
                continue

            # Calculate new position based on current direction
            new_x, new_y = marble.x, marble.y
            if marble.direction == "down":
                new_y += 1
            elif marble.direction == "left":
                new_x -= 1
                # After moving left, check if we should go down
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    next_component = self.components[new_y][new_x]
                    if next_component.type not in [ComponentType.RAMP_LEFT, ComponentType.RAMP_RIGHT]:
                        marble.direction = "down"
            elif marble.direction == "right":
                new_x += 1
                # After moving right, check if we should go down
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    next_component = self.components[new_y][new_x]
                    if next_component.type not in [ComponentType.RAMP_LEFT, ComponentType.RAMP_RIGHT]:
                        marble.direction = "down"

            # Check if new position is valid
            if (0 <= new_x < self.width and
                    0 <= new_y < self.height):
                new_component = self.components[new_y][new_x]

                # Check for collisions with other marbles
                if self.check_collision(new_x, new_y):
                    marble.is_moving = False
                    continue

                # Update position and handle component interactions
                self.components[marble.y][marble.x].is_occupied = False
                marble.x, marble.y = new_x, new_y
                self.components[new_y][new_x].is_occupied = True

                # Get current component after movement
                component = self.components[marble.y][marble.x]

                # Handle component interactions
                if component.type == ComponentType.RAMP_LEFT:
                    marble.direction = "left"
                elif component.type == ComponentType.RAMP_RIGHT:
                    marble.direction = "right"
                elif component.type == ComponentType.BIT_LEFT:
                    marble.direction = "right"
                    component.type = ComponentType.BIT_RIGHT
                elif component.type == ComponentType.BIT_RIGHT:
                    marble.direction = "left"
                    component.type = ComponentType.BIT_LEFT
                elif component.type == ComponentType.CROSSOVER:
                    if marble.direction == "down":
                        marble.direction = "left"
                    elif marble.direction == "left":
                        marble.direction = "down"
                    elif marble.direction == "right":
                        marble.direction = "down"
                elif component.type == ComponentType.LEVER_BLUE:
                    self.set_active_launcher("left")
                    self.launch_marble("blue")
                    marble.is_moving = False
                    self.active_launcher = None
                elif component.type == ComponentType.LEVER_RED:
                    self.set_active_launcher("right")
                    self.launch_marble("red")
                    marble.is_moving = False
                    self.active_launcher = None
                elif component.type == ComponentType.INTERCEPTOR:
                    marble.is_moving = False
                    # Count marble by color
                    if marble.color == "red":
                        self.red_marbles += 1
                    else:
                        self.blue_marbles += 1
                    marbles_to_remove.append(marble)
            else:
                # Marble is out of bounds, count it before removing
                if marble.color == "red":
                    self.red_marbles += 1
                else:
                    self.blue_marbles += 1
                marbles_to_remove.append(marble)

        # Remove marbles that went out of bounds or hit the interceptor
        for marble in marbles_to_remove:
            self.components[marble.y][marble.x].is_occupied = False
            self.marbles.remove(marble)

    def get_marble_counts(self) -> Dict[str, int]:
        """Get the current marble counts"""
        return {
            "red": self.red_marbles,
            "blue": self.blue_marbles
        }

    def reset(self) -> None:
        """Reset the game board"""
        self.marbles = []
        self.red_marbles = 0
        self.blue_marbles = 0
        self.initialize_board()