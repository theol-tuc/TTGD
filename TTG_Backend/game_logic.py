from typing import List, Tuple, Optional
import numpy as np
from enum import Enum


class ComponentType(Enum):
    EMPTY = 0
    RED_MARBLE = 1
    RAMP_LEFT = 2  # Blue ramp directing left
    RAMP_RIGHT = 3  # Red ramp directing right
    CROSSOVER = 4  # Allows marbles to pass over each other
    INTERCEPTOR = 5  # Stops marbles
    RED_LAUNCHER = 6  # Drops marbles from top
    BIT_LEFT = 7  # Bit component 
    BIT_RIGHT = 8  # Bit component
    RED_TRIGGER = 9
    BLUE_TRIGGER = 10
    BLUE_MARBLE = 11
    BLUE_LAUNCHER = 12  # Drops blue marbles from top


class Component:
    def __init__(self, type: ComponentType, x: int, y: int):
        self.type = type
        self.x = x
        self.y = y
        self.is_occupied = False

class Marble:
    def __init__(self, x: int, y: int, color: str = "red"):
        self.x = x
        self.y = y
        self.is_moving = False
        self.direction = "down"  # Default direction for falling
        self.color = color  # "red" or "blue"


class GameBoard:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.marbles: List[Marble] = []
        self.components: List[List[Component]] = [[Component(ComponentType.EMPTY, x, y)
                                                   for x in range(width)]
                                                  for y in range(height)]
        # Initialize two launchers - left and right
        self.left_launcher = (2, 0)  # Left launcher position
        self.right_launcher = (8, 0)  # Right launcher position
        self.active_launcher = None  # Will be set by trigger
        # Track total marbles by color
        self.red_marbles = 0
        self.blue_marbles = 0

    def reset(self) -> None:
        """Reset the game board to its initial state"""
        self.marbles.clear()
        self.active_launcher = None
        self.red_marbles = 0
        self.blue_marbles = 0
        self.components = [[Component(ComponentType.EMPTY, x, y)
                          for x in range(self.width)]
                         for y in range(self.height)]
        # Re-add launchers after reset
        self.add_component(ComponentType.LAUNCHER, self.left_launcher[0], self.left_launcher[1])
        self.add_component(ComponentType.LAUNCHER, self.right_launcher[0], self.right_launcher[1])

    def add_component(self, type: ComponentType, x: int, y: int) -> bool:
        """Add a component to the board if the position is valid and empty"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.components[y][x] = Component(type, x, y)
            return True
        return False

    def add_marble(self, x: int, y: int, color: str = "red") -> bool:
        """Add a marble to the board if the position is valid and empty or is a launcher"""
        if 0 <= x < self.width and 0 <= y < self.height:
            component = self.components[y][x]
            if (component.type == ComponentType.EMPTY or component.type == ComponentType.LAUNCHER) and not component.is_occupied:
                marble = Marble(x, y, color)
                marble.is_moving = True  # Initialize marble as moving
                self.marbles.append(marble)
                component.is_occupied = True
                return True
        return False

    def launch_marble(self, color: str = "red") -> bool:
        """Launch a marble from the active launcher"""
        if self.active_launcher == "left":
            x, y = self.left_launcher
            return self.add_marble(x, y, color)
        elif self.active_launcher == "right":
            x, y = self.right_launcher
            return self.add_marble(x, y, color)
        return False

    def set_active_launcher(self, launcher: str) -> None:
        """Set which launcher is active (left or right)"""
        if launcher in ["left", "right"]:
            self.active_launcher = launcher

    def check_collision(self, x: int, y: int) -> bool:
        """Check if a position is occupied by another marble"""
        for marble in self.marbles:
            if marble.x == x and marble.y == y:
                return True
        return False

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
            elif marble.direction == "right":
                new_x += 1

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

    def get_board_state(self) -> List[List[int]]:
        """Return the current state of the board"""
        return [[component.type.value for component in row] for row in self.components]

    def get_marble_positions(self) -> List[Tuple[int, int]]:
        """Return the positions of all marbles"""
        return [(marble.x, marble.y) for marble in self.marbles]

    def get_component_positions(self) -> List[Tuple[int, int, int]]:
        """Return the positions and types of all components"""
        components = []
        for y in range(self.height):
            for x in range(self.width):
                if self.components[y][x].type != ComponentType.EMPTY:
                    components.append((x, y, self.components[y][x].type.value))
        return components

    def get_marble_counts(self) -> dict:
        """Return the total counts of red and blue marbles"""
        return {
            "red": self.red_marbles,
            "blue": self.blue_marbles
        }