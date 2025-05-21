from typing import Dict, Any
from game_logic import GameBoard, ComponentType, Marble
from ai_service import AIService

class AIManager:
    def __init__(self):
        self.ai_service = AIService()

    def convert_game_state_to_board(self, game_state: Dict[str, Any]) -> GameBoard:
        """
        Convert game state dictionary to GameBoard object.
        """
        # Create new board
        board = GameBoard(8, 8)  # Standard 8x8 board
        board.initialize_board()  # Initialize the board structure

        # Set marbles
        board.set_number_of_marbles(
            game_state.get('red_marbles', 8),
            game_state.get('blue_marbles', 8)
        )

        # Set launcher position
        if 'active_launcher' in game_state:
            board.set_active_launcher(game_state['active_launcher'])

        # Add components
        if 'components' in game_state:
            for row_idx, row in enumerate(game_state['components']):
                for col_idx, component in enumerate(row):
                    if component and component.get('type'):
                        try:
                            comp_type = ComponentType(component['type'])
                            board.add_component(comp_type, col_idx, row_idx)  # Fixed x,y order
                        except ValueError:
                            print(f"Invalid component type: {component['type']}")

        return board

    def get_ai_move(self, game_state: Dict[str, Any], challenge_id: str = None) -> Dict[str, Any]:
        """
        Get AI's next move based on current game state and challenge context.
        """
        try:
            # Debug print
            #print("Received game state:", game_state)
            
            # Convert game state to board
            board = self.convert_game_state_to_board(game_state)
            
            # Debug print
            print("Converted board components:")
            for y in range(board.height):
                for x in range(board.width):
                    component = board.components[y][x]
                    if component.type not in [ComponentType.EMPTY, ComponentType.GRAY_SPACE, ComponentType.INVALID]:
                        print(f"Component at ({x}, {y}): {component.type.value}")
            
            # Get AI move with challenge context
            return self.ai_service.get_ai_move(board, challenge_id)
        except Exception as e:
            print(f"Error in AIManager.get_ai_move: {str(e)}")
            raise

    def get_ai_explanation(self, game_state: Dict[str, Any], move: Dict[str, Any], challenge_id: str = None) -> str:
        """
        Get AI's explanation for a specific move in the context of a challenge.
        """
        # Convert game state to board
        board = self.convert_game_state_to_board(game_state)
        
        # Get AI explanation with challenge context
        return self.ai_service.get_ai_explanation(board, move, challenge_id)
