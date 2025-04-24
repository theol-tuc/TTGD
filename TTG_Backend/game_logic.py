from typing import List, Tuple, Optional, Dict
#import numpy as np
from enum import Enum


class ComponentType(Enum):
    EMPTY = "empty" #spaces where you can place elements
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
    GRAY_SPACE = "gray_space" #spaces where you can only place gears
    LEVER_BLUE = "lever_blue"
    LEVER_RED = "lever_red"
    GEAR = "gear" # Basic gear that rotates marbles
    GEAR_BIT_LEFT = "gear_bit_left" # Left gear bit
    GEAR_BIT_RIGHT = "gear_bit_right" # Right gear bit


class Component:
    def __init__(self, type: ComponentType, x: int, y: int):
        self.type = type
        self.x = x
        self.y = y
        self.is_occupied = False
        # Gear properties - simplified
        self.is_gear = type == ComponentType.GEAR
        self.is_gear_bit = type == ComponentType.GEAR_BIT_LEFT or type == ComponentType.GEAR_BIT_RIGHT
        self.gear_rotation = 0  # 0, 90, 180, 270 degrees
        self.gear_bit_state = False  # False = 0, True = 1

class Marble:
    def __init__(self, color: str, x: int, y: int, direction: str):
        self.color = color
        self.x = x
        self.y = y
        self.direction = direction  # "left", "right", "up", "down"
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

        #Set up the diamond pattern
        self.setup_diamond_pattern()

        # Set vertical borders
        for y in range(self.height):
            self.components[y][0].type = ComponentType.BORDER_VERTICAL
            self.components[y][14].type = ComponentType.BORDER_VERTICAL

        # Set horizontal border (last row)
        for x in range(self.width):
            self.components[16][x].type = ComponentType.BORDER_HORIZONTAL

        # Add levers at the bottom
        self.components[14][6].type = ComponentType.LEVER_BLUE
        self.components[14][8].type = ComponentType.LEVER_RED

        # Add corners
        self.components[16][0].type = ComponentType.CORNER_LEFT
        self.components[16][14].type = ComponentType.CORNER_RIGHT

        # Add launchers at the top
        self.components[2][5].type = ComponentType.LAUNCHER  # Left launcher
        self.components[2][9].type = ComponentType.LAUNCHER  # Right launcher

        for y in range (1, self.width-1):
            self.components[13][y].type = ComponentType.INVALID

        self.components[13][7].type = ComponentType.EMPTY
        self.components[14][7].type = ComponentType.INVALID
        self.components[15][7].type = ComponentType.INVALID

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

        # Row 4 (index 3)
        for x in range(1, self.width - 1):
            if x in [1,2,3,7,11,12,13]:
                self.components[3][x].type = ComponentType.INVALID
            elif x % 2 == 0:
                self.components[3][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[3][x].type = ComponentType.EMPTY

        # Row 5 (index 4)
        for x in range(1, self.width):
            if x in [1,2,12,13]:
                self.components[4][x].type = ComponentType.INVALID
            elif x % 2 == 1:
                self.components[4][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[4][x].type = ComponentType.EMPTY



        # Middle rows
        for y in range(5, 13):
            for x in range(2,14):
                if (x + y) % 2 == 1:
                    self.components[y][x].type = ComponentType.GRAY_SPACE
                else:
                    self.components[y][x].type = ComponentType.EMPTY
            self.components[y][1].type = ComponentType.INVALID
            self.components[y][13].type = ComponentType.INVALID

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
            x = 5  # Left launcher position
            direction = "right"
        else:
            x = 9  # Right launcher position
            direction = "left"
        y = 0
        
        # Check if position is valid
        if 0 <= x < self.width and 0 <= y < self.height:
            if not self.check_collision(x, y):
                self.marbles.append(Marble(color, x, y, direction))
                self.components[y][x].is_occupied = True
                print(f"Launched marble at ({x}, {y}) with direction {direction}")

    def check_collision(self, x: int, y: int) -> bool:
        """Check if a position is occupied"""
        return self.components[y][x].is_occupied
    
    def set_bit_type(self, component: Component) -> None:
        """
        Set the correct bit type based on the current component type.
        Flips BIT_LEFT to BIT_RIGHT and BIT_RIGHT to BIT_LEFT.
        Updates the component type and returns the new direction for the marble.
        """
        if component.type == ComponentType.BIT_LEFT:
            component.type = ComponentType.BIT_RIGHT
            return "right"
        elif component.type == ComponentType.BIT_RIGHT:
            component.type = ComponentType.BIT_LEFT
            return "left"
        return None  # If no change is made, return None
        
    def flip_gears(self, x: int, y: int, visited=None) -> None:
        """
        Flip all connected gears starting from position (x, y).
        This is a depth-first search to find all connected gears.
        """
        if visited is None:
            visited = set()
            
        # Mark current position as visited
        visited.add((x, y))
        
        # Get the current component
        component = self.components[y][x]
        
        # If not a gear or gear bit, return
        if not (component.is_gear or component.is_gear_bit):
            return
            
        # Flip gear bits
        if component.type == ComponentType.GEAR_BIT_LEFT:
            component.type = ComponentType.GEAR_BIT_RIGHT
            print(f"Flipped gear bit at ({x}, {y}) from LEFT to RIGHT")
        elif component.type == ComponentType.GEAR_BIT_RIGHT:
            component.type = ComponentType.GEAR_BIT_LEFT
            print(f"Flipped gear bit at ({x}, {y}) from RIGHT to LEFT")
            
        # Check adjacent cells (up, right, down, left)
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check if the new position is valid and not visited
            if (0 <= new_x < self.width and 0 <= new_y < self.height and 
                (new_x, new_y) not in visited):
                # Recursively flip connected gears
                self.flip_gears(new_x, new_y, visited)

    def update_marble_positions(self) -> None:
        """Update all marble positions based on components and physics"""
        marbles_to_remove = []

        for marble in self.marbles:
            if not marble.is_moving:
                continue
                
            print(f"Marble at ({marble.x}, {marble.y}) is moving {marble.direction}")
            
            current_component = self.components[marble.y][marble.x]
            
            if current_component.type == ComponentType.RAMP_LEFT:
                if (marble.y + 1 < self.height and 
                    marble.x - 1 >= 0 and 
                    not self.check_collision(marble.x - 1, marble.y + 1)):
                    marble.direction = "left"
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.y += 1
                    marble.x -= 1
                    self.components[marble.y][marble.x].is_occupied = True
            elif current_component.type == ComponentType.RAMP_RIGHT:
                if (marble.y + 1 < self.height and 
                    marble.x + 1 < self.width and 
                    not self.check_collision(marble.x + 1, marble.y + 1)):
                    marble.direction = "right"
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.y += 1
                    marble.x += 1
                    self.components[marble.y][marble.x].is_occupied = True
            elif current_component.type == ComponentType.BIT_LEFT:
                marble.direction = "right"
                self.set_bit_type(current_component)
                new_x, new_y = marble.x, marble.y
                if new_x + 1 < self.width and not self.check_collision(new_x + 1, new_y):
                    new_x += 1
                elif (new_y + 1 < self.height and new_x + 1 < self.width and 
                      not self.check_collision(new_x + 1, new_y + 1)):
                    new_x += 1
                    new_y += 1
                else:
                    marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.BIT_RIGHT:
                marble.direction = "left"
                self.set_bit_type(current_component)
                new_x, new_y = marble.x, marble.y
                if new_x - 1 >= 0 and not self.check_collision(new_x - 1, new_y):
                    new_x -= 1
                elif (new_y + 1 < self.height and new_x - 1 >= 0 and 
                      not self.check_collision(new_x - 1, new_y + 1)):
                    new_x -= 1
                    new_y += 1
                else:
                    marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.CROSSOVER:
                new_x, new_y = marble.x, marble.y
                if marble.direction == "left":
                    if new_x - 1 >= 0 and not self.check_collision(new_x - 1, new_y):
                        new_x -= 1
                    elif (new_y + 1 < self.height and new_x - 1 >= 0 and 
                          not self.check_collision(new_x - 1, new_y + 1)):
                        new_x -= 1
                        new_y += 1
                    else:
                        marble.is_moving = False
                else:
                    if new_x + 1 < self.width and not self.check_collision(new_x + 1, new_y):
                        new_x += 1
                    elif (new_y + 1 < self.height and new_x + 1 < self.width and 
                          not self.check_collision(new_x + 1, new_y + 1)):
                        new_x += 1
                        new_y += 1
                    else:
                        marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.GEAR:
                # Flip all connected gears
                self.flip_gears(marble.x, marble.y)
                
                # Calculate new position based on current direction
                new_x, new_y = marble.x, marble.y
                if marble.direction == "left":
                    if new_x - 1 >= 0 and not self.check_collision(new_x - 1, new_y):
                        new_x -= 1
                    elif (new_y + 1 < self.height and new_x - 1 >= 0 and 
                          not self.check_collision(new_x - 1, new_y + 1)):
                        new_x -= 1
                        new_y += 1
                    else:
                        marble.is_moving = False
                elif marble.direction == "right":
                    if new_x + 1 < self.width and not self.check_collision(new_x + 1, new_y):
                        new_x += 1
                    elif (new_y + 1 < self.height and new_x + 1 < self.width and 
                          not self.check_collision(new_x + 1, new_y + 1)):
                        new_x += 1
                        new_y += 1
                    else:
                        marble.is_moving = False
                elif marble.direction == "up":
                    if new_y - 1 >= 0 and not self.check_collision(new_x, new_y - 1):
                        new_y -= 1
                    else:
                        marble.is_moving = False
                elif marble.direction == "down":
                    if new_y + 1 < self.height and not self.check_collision(new_x, new_y + 1):
                        new_y += 1
                    else:
                        marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.GEAR_BIT_LEFT:
                # Flip all connected gears and change direction
                self.flip_gears(marble.x, marble.y)
                marble.direction = "right"
                
                # Calculate new position based on new direction
                new_x, new_y = marble.x, marble.y
                if new_x + 1 < self.width and not self.check_collision(new_x + 1, new_y):
                    new_x += 1
                elif (new_y + 1 < self.height and new_x + 1 < self.width and 
                      not self.check_collision(new_x + 1, new_y + 1)):
                    new_x += 1
                    new_y += 1
                else:
                    marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.GEAR_BIT_RIGHT:
                # Flip all connected gears and change direction
                self.flip_gears(marble.x, marble.y)
                marble.direction = "left"
                
                # Calculate new position based on new direction
                new_x, new_y = marble.x, marble.y
                if new_x - 1 >= 0 and not self.check_collision(new_x - 1, new_y):
                    new_x -= 1
                elif (new_y + 1 < self.height and new_x - 1 >= 0 and 
                      not self.check_collision(new_x - 1, new_y + 1)):
                    new_x -= 1
                    new_y += 1
                else:
                    marble.is_moving = False
                
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
            elif current_component.type == ComponentType.LEVER_BLUE:
                self.set_active_launcher("left")
                self.launch_marble("blue")
                marble.is_moving = False
                marbles_to_remove.append(marble)
            elif current_component.type == ComponentType.LEVER_RED:
                self.set_active_launcher("right")
                self.launch_marble("red")
                marble.is_moving = False
                marbles_to_remove.append(marble)
            elif current_component.type == ComponentType.INTERCEPTOR:
                marble.is_moving = False
                if marble.color == "red":
                    self.red_marbles += 1
                else:
                    self.blue_marbles += 1
                marbles_to_remove.append(marble)
            elif current_component.type in [
                ComponentType.BORDER_VERTICAL,
                ComponentType.BORDER_HORIZONTAL,
                ComponentType.BORDER_DIAGONAL_LEFT,
                ComponentType.BORDER_DIAGONAL_RIGHT,
                ComponentType.CORNER_LEFT,
                ComponentType.CORNER_RIGHT
            ]:
                marble.is_moving = False
            else:  # EMPTY or other components
                # Calculate new position based on current direction and gravity
                new_x, new_y = marble.x, marble.y
                
                # First try to move down (gravity)
                if new_y + 1 < self.height and not self.check_collision(new_x, new_y + 1):
                    new_y += 1
                else:
                    # If can't move down, try moving horizontally based on direction
                    if marble.direction == "left":
                        if new_x - 1 >= 0 and not self.check_collision(new_x - 1, new_y):
                            new_x -= 1
                        else:
                            # If blocked, try to move down-left if possible
                            if (new_y + 1 < self.height and new_x - 1 >= 0 and 
                                not self.check_collision(new_x - 1, new_y + 1)):
                                new_x -= 1
                                new_y += 1
                            else:
                                marble.is_moving = False
                    elif marble.direction == "right":
                        if new_x + 1 < self.width and not self.check_collision(new_x + 1, new_y):
                            new_x += 1
                        else:
                            # If blocked, try to move down-right if possible
                            if (new_y + 1 < self.height and new_x + 1 < self.width and 
                                not self.check_collision(new_x + 1, new_y + 1)):
                                new_x += 1
                                new_y += 1
                            else:
                                marble.is_moving = False
                    elif marble.direction == "up":
                        if new_y - 1 >= 0 and not self.check_collision(new_x, new_y - 1):
                            new_y -= 1
                        else:
                            marble.is_moving = False
                    elif marble.direction == "down":
                        if new_y + 1 < self.height and not self.check_collision(new_x, new_y + 1):
                            new_y += 1
                        else:
                            marble.is_moving = False
                
                # Update position if still moving
                if marble.is_moving and 0 <= new_x < self.width and 0 <= new_y < self.height:
                    self.components[marble.y][marble.x].is_occupied = False
                    marble.x, marble.y = new_x, new_y
                    self.components[new_y][new_x].is_occupied = True
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