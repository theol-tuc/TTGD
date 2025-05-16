import numpy as np
from typing import List, Tuple, Dict
from .game_logic import GameBoard, ComponentType

class BoardEncoder:
    """Converts the game board state into LLM-friendly text format"""
    
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.num_component_types = len(ComponentType)
        
    def encode_board(self, board: GameBoard) -> np.ndarray:
        """Encode the board state into a tensor"""
        # Create a one-hot encoded representation
        encoded = np.zeros((self.height, self.width, self.num_component_types), dtype=np.float32)
        
        # Encode components
        for comp in board.components:
            x, y = comp.position
            if 0 <= x < self.width and 0 <= y < self.height:
                encoded[y, x, comp.type.value] = 1.0
        
        # Encode marbles
        for marble in board.marbles:
            x, y = marble.position
            if 0 <= x < self.width and 0 <= y < self.height:
                # Add marble channel
                encoded[y, x, -1] = 1.0
        
        return encoded
    
    def decode_board(self, encoded: np.ndarray) -> GameBoard:
        """Decode a tensor back into a GameBoard"""
        board = GameBoard(self.width, self.height)
        
        # Decode components
        for y in range(self.height):
            for x in range(self.width):
                component_type = np.argmax(encoded[y, x, :-1])  # Exclude marble channel
                if component_type != ComponentType.EMPTY.value:
                    board.add_component(ComponentType(component_type), x, y)
        
        # Decode marbles
        for y in range(self.height):
            for x in range(self.width):
                if encoded[y, x, -1] > 0.5:  # Marble present
                    board.add_marble()
        
        return board
    
    def encode_sequence(self, boards: List[GameBoard]) -> np.ndarray:
        """Encode a sequence of board states"""
        return np.stack([self.encode_board(board) for board in boards])
    
    def decode_sequence(self, encoded_sequence: np.ndarray) -> List[GameBoard]:
        """Decode a sequence of encoded board states"""
        return [self.decode_board(encoded) for encoded in encoded_sequence]
    
    def get_adjacency_matrix(self, board: GameBoard) -> np.ndarray:
        """Get the adjacency matrix for the board's components"""
        n = len(board.components)
        adj_matrix = np.zeros((n, n), dtype=np.float32)
        
        for i, comp1 in enumerate(board.components):
            for j, comp2 in enumerate(board.components):
                if i != j:
                    x1, y1 = comp1.position
                    x2, y2 = comp2.position
                    
                    # Check if components are adjacent
                    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                        adj_matrix[i, j] = 1.0
        
        return adj_matrix
    
    def get_component_features(self, board: GameBoard) -> np.ndarray:
        """Get feature vectors for each component"""
        n = len(board.components)
        features = np.zeros((n, self.num_component_types + 2), dtype=np.float32)
        
        for i, comp in enumerate(board.components):
            # One-hot encode component type
            features[i, comp.type.value] = 1.0
            
            # Add position features
            features[i, -2] = comp.position[0] / self.width
            features[i, -1] = comp.position[1] / self.height
        
        return features

    @staticmethod
    def encode_board(board: GameBoard) -> str:
        """Convert the game board state to a text description"""
        return f"""Turing Tumble Game State:

Board Layout:
{BoardEncoder._encode_board_layout(board)}

Active Components:
{BoardEncoder._encode_components(board)}

Game Status:
{BoardEncoder._encode_game_status(board)}

Possible Actions:
{BoardEncoder._encode_possible_actions()}"""

    @staticmethod
    def _encode_board_layout(board: GameBoard) -> str:
        """Create a text representation of the board layout"""
        layout = []
        for y in range(board.height):
            row = []
            for x in range(board.width):
                component = board.board[y][x]
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
                component = board.board[y][x]
                if component.type != ComponentType.EMPTY:
                    components.append(f"- {component.type.name} at position ({x}, {y})")
        return "\n".join(components) if components else "No active components"

    @staticmethod
    def _encode_game_status(board: GameBoard) -> str:
        """Create a text description of the game status"""
        return f"- Active components placed: {sum(1 for row in board.board for comp in row if comp.type != ComponentType.EMPTY)}"

    @staticmethod
    def _encode_possible_actions() -> str:
        """Create a text description of possible actions"""
        actions = [
            "1. Place a new component:",
            "   - RAMP_LEFT (\\)",
            "   - RAMP_RIGHT (/)",
            "   - CROSSOVER (+)",
            "   - INTERCEPTOR (X)",
            "2. Drop a marble",
            "3. Reset the board"
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

# Example usage
if __name__ == "__main__":
    # Create a test board
    board = GameBoard()
    
    # Add some test components
    board.add_component(ComponentType.GEAR, 7, 7)
    board.add_component(ComponentType.BIT_LEFT, 6, 6)
    board.add_component(ComponentType.RAMP_LEFT, 8, 8)
    
    # Encode the board
    encoded_state = BoardEncoder.encode_board(board)
    print(encoded_state)
    
    # Print game rules
    print("\nGame Rules:")
    print(BoardEncoder.encode_game_rules()) 