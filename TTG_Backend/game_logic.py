from typing import List, Tuple, Optional
import numpy as np
from enum import Enum


class ComponentType(Enum):
    EMPTY = 0
    MARBLE = 1
    RAMP_LEFT = 2  # Blue ramp directing left
    RAMP_RIGHT = 3  # Red ramp directing right
    CROSSOVER = 4  # Allows marbles to pass over each other
    INTERCEPTOR = 5  # Stops marbles
    LAUNCHER = 6  # Drops marbles from top
    BIT_LEFT = 7  # Bit component 
    BIT_RIGHT = 8  # Bit component


class Component:
    def __init__(self, type: ComponentType, x: int, y: int):
        self.type = type
        self.x = x
        self.y = y
        self.is_occupied = False

class Marble:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_moving = False
        self.direction = "down"  # Default direction for falling


class GameBoard:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.marbles: List[Marble] = []
        self.components: List[List[Component]] = [[Component(ComponentType.EMPTY, x, y)
                                                   for x in range(width)]
                                                  for y in range(height)]
        self.launchers: List[Tuple[int, int]] = []  # Positions of launchers
        self.score = 0

    def reset(self) -> None:
        """Reset the game board to its initial state"""
        self.marbles.clear()
        self.launchers.clear()
        self.score = 0
        self.components = [[Component(ComponentType.EMPTY, x, y)
                          for x in range(self.width)]
                         for y in range(self.height)]

    def add_component(self, type: ComponentType, x: int, y: int) -> bool:
        """Add a component to the board if the position is valid and empty"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if type == ComponentType.LAUNCHER:
                self.launchers.append((x, y))
            self.components[y][x] = Component(type, x, y)
            return True
        return False

    def add_marble(self, x: int, y: int) -> bool:
        """Add a marble to the board if the position is valid and empty"""
        if 0 <= x < self.width and 0 <= y < self.height:
            component = self.components[y][x]
            if component.type == ComponentType.EMPTY and not component.is_occupied:
                marble = Marble(x, y)
                marble.is_moving = True  # Initialize marble as moving
                self.marbles.append(marble)
                component.is_occupied = True
                return True
        return False

    def launch_marble(self, launcher_index: int) -> bool:
        """Launch a marble from a launcher"""
        if 0 <= launcher_index < len(self.launchers):
            x, y = self.launchers[launcher_index]
            return self.add_marble(x, y)
        return False

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

            # Get current component
            component = self.components[marble.y][marble.x]

            # Default to moving down unless ramp changes it
            direction = "down"

            # Handle component interactions
            if component.type == ComponentType.BIT_LEFT:
                direction = "right"
                component.type = ComponentType.BIT_RIGHT
            elif component.type == ComponentType.BIT_RIGHT:
                direction = "left"
                component.type = ComponentType.BIT_LEFT
            if component.type == ComponentType.RAMP_LEFT:
                direction = "left"
            elif component.type == ComponentType.RAMP_RIGHT:
                direction = "right"
            elif component.type == ComponentType.INTERCEPTOR:
                marble.is_moving = False
                self.score += 1
                continue

            # Calculate new position based on current direction
            new_x, new_y = marble.x, marble.y
            if direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1

            # Check if new position is valid
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                new_component = self.components[new_y][new_x]

                if self.check_collision(new_x, new_y):
                    marble.is_moving = False
                    continue

                # Update positions if new spot is empty or a crossover
                if (new_component.type == ComponentType.EMPTY or
                        new_component.type == ComponentType.CROSSOVER or
                        new_component.type == ComponentType.RAMP_LEFT or
                        new_component.type == ComponentType.RAMP_RIGHT):
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    marble.direction = direction  # update direction here
                    self.components[new_y][new_x].is_occupied = True
                else:
                    marble.is_moving = False
            else:
                marbles_to_remove.append(marble)

        # Remove marbles that went out of bounds
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

    def get_score(self) -> int:
        """Return the current game score"""
        return self.score