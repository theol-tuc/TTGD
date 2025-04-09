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
                self.marbles.append(Marble(x, y))
                component.is_occupied = True
                return True
        return False

    def launch_marble(self, launcher_index: int) -> bool:
        """Launch a marble from a launcher"""
        if 0 <= launcher_index < len(self.launchers):
            x, y = self.launchers[launcher_index]
            return self.add_marble(x, y)
        return False

    def update_marble_positions(self) -> None:
        """Update all marble positions based on components and physics"""
        for marble in self.marbles:
            if not marble.is_moving:
                continue

            component = self.components[marble.y][marble.x]

            # Handle component interactions
            if component.type == ComponentType.RAMP_LEFT:
                marble.direction = "left"
            elif component.type == ComponentType.RAMP_RIGHT:
                marble.direction = "right"
            elif component.type == ComponentType.INTERCEPTOR:
                marble.is_moving = False
                continue
            elif component.type == ComponentType.CROSSOVER:
                # Allow marble to continue in its current direction
                pass

            # Calculate new position based on direction
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

                # Update positions if new spot is empty or a crossover
                if (new_component.type == ComponentType.EMPTY or
                        new_component.type == ComponentType.CROSSOVER):
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
                else:
                    marble.is_moving = False

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