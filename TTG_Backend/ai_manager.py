from typing import Dict, Any
from game_logic import GameBoard
from ai_service import AIService

class AIManager:
    def __init__(self):
        self.ai_service = AIService()

    def get_ai_move(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get AI's next move based on current game state
        """
        # Convert game state dict to GameBoard object
        board = GameBoard()
        # TODO: Convert game_state dict to board state
        # This is a placeholder - we need to implement the conversion
        
        # Get move from AI service
        return self.ai_service.get_ai_move(board)

    def get_ai_explanation(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> str:
        """
        Get AI's explanation for a specific move
        """
        # Convert game state dict to GameBoard object
        board = GameBoard()
        # TODO: Convert game_state dict to board state
        # This is a placeholder - we need to implement the conversion
        
        # Get explanation from AI service
        return self.ai_service.get_ai_explanation(board, move) 