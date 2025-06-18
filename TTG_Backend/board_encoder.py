from typing import List, Dict, Any
from game_logic import GameBoard, ComponentType

class BoardEncoder:
    """Converts the game board state into LLM-friendly text format"""
    
    @staticmethod
    def encode_board(board: GameBoard) -> str:
        """Convert the game board state to a text description"""
        return f"""Turing Tumble Game State:

Board Layout:
{BoardEncoder._encode_board_layout(board)}

Active Components:
{BoardEncoder._encode_components(board)}

Marble States:
{BoardEncoder._encode_marbles(board)}

Game Status:
- Active Launcher: {board.active_launcher}
- Red Marbles: {board.red_marbles}
- Blue Marbles: {board.blue_marbles}

Possible Actions:
{BoardEncoder._encode_possible_actions(board)}"""

    @staticmethod
    def _encode_board_layout(board: GameBoard) -> str:
        """Create a text representation of the board layout"""
        layout = []
        for y in range(board.height):
            row = []
            for x in range(board.width):
                component = board.components[y][x]
                if component.type == ComponentType.EMPTY:
                    row.append(".")
                elif component.type == ComponentType.GEAR:
                    row.append("G")
                elif component.type == ComponentType.BIT_LEFT:
                    row.append("L")
                elif component.type == ComponentType.BIT_RIGHT:
                    row.append("R")
                elif component.type == ComponentType.RAMP_LEFT:
                    row.append("\\")
                elif component.type == ComponentType.RAMP_RIGHT:
                    row.append("/")
                elif component.type == ComponentType.CROSSOVER:
                    row.append("X")
                elif component.type == ComponentType.INTERCEPTOR:
                    row.append("I")
                elif component.type == ComponentType.LAUNCHER:
                    row.append("S")
                elif component.type == ComponentType.LEVER_BLUE:
                    row.append("B")
                elif component.type == ComponentType.LEVER_RED:
                    row.append("r")
                elif component.type == ComponentType.GRAY_SPACE:
                    row.append("#")
                else:
                    row.append(" ")
            layout.append("".join(row))
        return "\n".join(layout)

    @staticmethod
    def _encode_components(board: GameBoard) -> str:
        """Create a text description of all active components"""
        components = []
        for y in range(board.height):
            for x in range(board.width):
                component = board.components[y][x]
                # Skip empty spaces, gray spaces, and invalid spaces
                if component.type in [ComponentType.EMPTY, ComponentType.GRAY_SPACE, ComponentType.INVALID]:
                    continue
                    
                # Skip border components unless they're special
                if component.type in [
                    ComponentType.BORDER_VERTICAL,
                    ComponentType.BORDER_HORIZONTAL,
                    ComponentType.BORDER_DIAGONAL_LEFT,
                    ComponentType.BORDER_DIAGONAL_RIGHT,
                    ComponentType.CORNER_LEFT,
                    ComponentType.CORNER_RIGHT
                ]:
                    continue
                
                # Format the component description
                desc = f"- {component.type.value} at position ({x}, {y})"
                
                # Add gear-specific details
                if component.is_gear:
                    desc += f" (rotation: {component.gear_rotation}°)"
                if component.is_gear_bit:
                    desc += f" (state: {'1' if component.gear_bit_state else '0'})"
                
                # Add special details for other components
                if component.type in [ComponentType.RAMP_LEFT, ComponentType.RAMP_RIGHT]:
                    desc += " (changes marble direction)"
                elif component.type in [ComponentType.BIT_LEFT, ComponentType.BIT_RIGHT]:
                    desc += " (stores binary state)"
                elif component.type == ComponentType.CROSSOVER:
                    desc += " (allows marbles to cross paths)"
                elif component.type == ComponentType.INTERCEPTOR:
                    desc += " (stops marbles)"
                elif component.type == ComponentType.LAUNCHER:
                    desc += " (launches marbles)"
                elif component.type in [ComponentType.LEVER_BLUE, ComponentType.LEVER_RED]:
                    desc += " (controls marble flow)"
                
                components.append(desc)
        
        return "\n".join(components) if components else "No active components"

    @staticmethod
    def _encode_marbles(board: GameBoard) -> str:
        """Create a text description of all marbles"""
        if not board.marbles:
            return "No marbles on the board"
        
        marbles = []
        for marble in board.marbles:
            state = "moving" if marble.is_moving else "stopped"
            marbles.append(f"- {marble.color} marble at ({marble.x}, {marble.y}), moving {marble.direction} ({state})")
        return "\n".join(marbles)

    @staticmethod
    def _encode_possible_actions(board: GameBoard) -> str:
        """Create a text description of possible actions"""
        actions = [
            "1. Place a new component:",
            "   - Gear (G)",
            "   - Bit (L/R)",
            "   - Ramp (\\/)",
            "   - Crossover (X)",
            "   - Interceptor (I)",
            "2. Launch a marble (if launcher is empty)",
            "3. Switch active launcher (left/right)",
            "4. Reset the board"
        ]
        return "\n".join(actions)

    @staticmethod
    def encode_game_rules() -> str:
        """Provide a text description of the game rules"""
        return """Turing Tumble Game Rules:

1. Board Layout:
   - 15x17 grid board
   - Two launchers at the top (left and right)
   - Gray spaces (#) can only hold gears
   - Empty spaces (.) can hold any component

2. Components:
   - Gear (G): Rotates marbles and can connect to other gears
   - Bit (L/R): Stores binary state (0/1)
   - Ramp (\\/): Changes marble direction
   - Crossover (X): Allows marbles to cross paths
   - Interceptor (I): Stops marbles

3. Marbles:
   - Red and blue marbles
   - Launch from either launcher
   - Follow gravity and component rules
   - Can trigger gear rotations and bit flips

4. Winning Conditions:
   - Complete the puzzle by achieving the target pattern
   - Use the minimum number of components
   - Follow any specific rules for the current puzzle"""