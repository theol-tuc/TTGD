import requests
import json
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard
from challenges import CHALLENGES
from prompting import prompt_manager

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
            # Convert board to game state
            game_state = {
                'components': board.get_components_state(),
                'red_marbles': board.red_marbles,
                'blue_marbles': board.blue_marbles,
                'active_launcher': board.active_launcher
            }

            # Generate appropriate prompt
            prompt = prompt_manager.generate_prompt(
                context_type='library' if challenge_id else 'matrix',
                game_state=game_state,
                challenge_id=challenge_id
            )

            # Send to LLM server
            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={
                    "prompt": prompt,
                    "board_state": self.board_encoder.encode_board(board)
                }
            )

            if response.status_code != 200:
                raise Exception(f"LLM server returned status code {response.status_code}")

            return response.json()

        except Exception as e:
            print(f"[AIService] Error getting AI move: {str(e)}")
            raise

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any], challenge_id: str = None) -> str:
        """
        Get AI's explanation for a specific move in the context of a challenge.
        """
        try:
            # Convert board to game state
            game_state = {
                'components': board.get_components_state(),
                'red_marbles': board.red_marbles,
                'blue_marbles': board.blue_marbles,
                'active_launcher': board.active_launcher
            }

            # Generate analysis prompt
            prompt = prompt_manager.generate_prompt(
                context_type='analysis',
                game_state=game_state,
                challenge_id=challenge_id
            )

            # Send to LLM server
            response = requests.post(
                f"{self.llm_server_url}/explain",
                json={
                    "prompt": prompt,
                    "board_state": self.board_encoder.encode_board(board),
                    "move": move
                }
            )

            if response.status_code != 200:
                raise Exception(f"LLM server returned status code {response.status_code}")

            return response.json().get('explanation', 'No explanation available')

        except Exception as e:
            print(f"[AIService] Error getting AI explanation: {str(e)}")
            raise
