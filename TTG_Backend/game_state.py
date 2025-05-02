from typing import Dict, List, Any
from game_logic import GameBoard, Component, Marble, ComponentType
import json

class GameStateSerializer:
    """Handles serialization and deserialization of the Turing Tumble game state"""
    
    @staticmethod
    def serialize_board(board: GameBoard) -> Dict[str, Any]:
        """Convert the game board state to a JSON-serializable dictionary"""
        return {
            "width": board.width,
            "height": board.height,
            "components": GameStateSerializer._serialize_components(board.components),
            "marbles": GameStateSerializer._serialize_marbles(board.marbles),
            "active_launcher": board.active_launcher,
            "red_marbles": board.red_marbles,
            "blue_marbles": board.blue_marbles
        }
    
    @staticmethod
    def _serialize_components(components: List[List[Component]]) -> List[List[Dict[str, Any]]]:
        """Convert the 2D array of components to a serializable format"""
        return [
            [
                {
                    "type": component.type.value,
                    "x": component.x,
                    "y": component.y,
                    "is_occupied": component.is_occupied,
                    "gear_rotation": component.gear_rotation,
                    "gear_bit_state": component.gear_bit_state
                }
                for component in row
            ]
            for row in components
        ]
    
    @staticmethod
    def _serialize_marbles(marbles: List[Marble]) -> List[Dict[str, Any]]:
        """Convert the list of marbles to a serializable format"""
        return [
            {
                "color": marble.color,
                "x": marble.x,
                "y": marble.y,
                "direction": marble.direction,
                "is_moving": marble.is_moving
            }
            for marble in marbles
        ]
    
    @staticmethod
    def to_json(board: GameBoard) -> str:
        """Convert the game board state to a JSON string"""
        return json.dumps(GameStateSerializer.serialize_board(board), indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> Dict[str, Any]:
        """Convert a JSON string back to a game state dictionary"""
        return json.loads(json_str)

# Example usage
if __name__ == "__main__":
    # Create a test board
    board = GameBoard()
    
    # Serialize to JSON
    json_state = GameStateSerializer.to_json(board)
    print("Serialized Game State:")
    print(json_state)
    
    # Deserialize back to dictionary
    state_dict = GameStateSerializer.from_json(json_state)
    print("\nDeserialized State Dictionary:")
    print(state_dict) 