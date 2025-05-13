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
    
    @staticmethod
    def from_json_to_board(json_str: str) -> GameBoard:
        """Convert a JSON string back to a GameBoard object"""
        state_dict = GameStateSerializer.from_json(json_str)
        return GameStateSerializer._deserialize_board(state_dict)
    
    @staticmethod
    def _deserialize_board(state_dict: Dict[str, Any]) -> GameBoard:
        """Convert a state dictionary to a GameBoard object"""
        board = GameBoard(state_dict["width"], state_dict["height"])
        
        # Deserialize components
        GameStateSerializer._deserialize_components(board, state_dict["components"])
        
        # Deserialize marbles
        GameStateSerializer._deserialize_marbles(board, state_dict["marbles"])
        
        # Set other properties
        board.active_launcher = state_dict["active_launcher"]
        board.red_marbles = state_dict["red_marbles"]
        board.blue_marbles = state_dict["blue_marbles"]
        
        return board
    
    @staticmethod
    def _deserialize_components(board: GameBoard, components_data: List[List[Dict[str, Any]]]) -> None:
        """Convert serialized components back to Component objects"""
        for y, row in enumerate(components_data):
            for x, component_data in enumerate(row):
                component_type = ComponentType(component_data["type"])
                component = Component(component_type, x, y)
                component.is_occupied = component_data["is_occupied"]
                component.gear_rotation = component_data["gear_rotation"]
                component.gear_bit_state = component_data["gear_bit_state"]
                board.components[y][x] = component
    
    @staticmethod
    def _deserialize_marbles(board: GameBoard, marbles_data: List[Dict[str, Any]]) -> None:
        """Convert serialized marbles back to Marble objects"""
        board.marbles = [
            Marble(
                color=marble_data["color"],
                x=marble_data["x"],
                y=marble_data["y"],
                direction=marble_data["direction"]
            )
            for marble_data in marbles_data
        ]
        for marble in board.marbles:
            marble.is_moving = marble_data["is_moving"]

# Example usage
if __name__ == "__main__":
    # Create a test board
    board = GameBoard()
    
    # Serialize to JSON
    json_state = GameStateSerializer.to_json(board)
    print("Serialized Game State:")
    print(json_state)
    
    # Deserialize back to board
    reconstructed_board = GameStateSerializer.from_json_to_board(json_state)
    print("\nReconstructed Board Properties:")
    print(f"Dimensions: {reconstructed_board.width}x{reconstructed_board.height}")
    print(f"Active Launcher: {reconstructed_board.active_launcher}")
    print(f"Marble Counts - Red: {reconstructed_board.red_marbles}, Blue: {reconstructed_board.blue_marbles}") 