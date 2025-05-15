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
        # Placeholder: use correct board dimensions
        board = GameBoard(8, 8)  # 👈 Fixed

        print("[AIManager] WARNING: Game state is not yet mapped to GameBoard.")

        return self.ai_service.get_ai_move(board)

    def get_ai_explanation(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> str:
        """
        Get AI's explanation for a specific move
        """
        board = GameBoard(8, 8)  # 👈 Fixed

        print("[AIManager] WARNING: Game state is not yet mapped to GameBoard.")

        return self.ai_service.get_ai_explanation(board, move)
