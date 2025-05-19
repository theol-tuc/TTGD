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

        # Set marbles
        if 'marbles' in game_state:
            board.set_number_of_marbles(
                game_state['marbles'].get('red', 8),
                game_state['marbles'].get('blue', 8)
            )

        # Set launcher position
        if 'launcher' in game_state:
            board.set_launcher(game_state['launcher'])

        # Add components
        if 'components' in game_state:
            for row_idx, row in enumerate(game_state['components']):
                for col_idx, component in enumerate(row):
                    if component and component.get('type'):
                        try:
                            comp_type = ComponentType(component['type'])
                            board.add_component(comp_type, row_idx, col_idx)
                        except ValueError:
                            print(f"Invalid component type: {component['type']}")

        return board

    def get_ai_move(self, game_state: Dict[str, Any], challenge_id: str = None) -> Dict[str, Any]:
        """
        Get AI's next move based on current game state and challenge context.
        """
        # Convert game state to board
        board = self.convert_game_state_to_board(game_state)
        
        # Get AI move with challenge context
        return self.ai_service.get_ai_move(board, challenge_id)

    def get_ai_explanation(self, game_state: Dict[str, Any], move: Dict[str, Any], challenge_id: str = None) -> str:
        """
        Get AI's explanation for a specific move in the context of a challenge.
        """
        # Convert game state to board
        board = self.convert_game_state_to_board(game_state)
        
        # Get AI explanation with challenge context
        return self.ai_service.get_ai_explanation(board, move, challenge_id)
