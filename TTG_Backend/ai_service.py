import requests
import json
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard
from challenges import CHALLENGES

class AIService:
    def __init__(self, llm_server_url: str = "http://localhost:8001"):
        self.llm_server_url = llm_server_url
        self.board_encoder = BoardEncoder()
        self.challenges = CHALLENGES

    def get_ai_move(self, board: GameBoard, challenge_id: str = None) -> Dict[str, Any]:
        """
        Get AI's next move based on current game state and challenge context.
        """
        try:
            # Get challenge context if challenge_id is provided
            challenge = self.challenges.get(challenge_id) if challenge_id else None
            
            # For now, return a simple move
            return {
                "action": "add_component",
                "parameters": {
                    "type": "ramp_right",
                    "x": 3,
                    "y": 5
                },
                "explanation": "Adding a ramp to guide the marble"
            }
        except Exception as e:
            print(f"[AIService] Error getting AI move: {str(e)}")
            raise

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any], challenge_id: str = None) -> str:
        """
        Get AI's explanation for a specific move in the context of a challenge.
        """
        try:
            # Get challenge context if challenge_id is provided
            challenge = self.challenges.get(challenge_id) if challenge_id else None
            
            # For now, return a simple explanation
            return "This move helps guide the marble in the desired direction."
        except Exception as e:
            print(f"[AIService] Error getting AI explanation: {str(e)}")
            raise
