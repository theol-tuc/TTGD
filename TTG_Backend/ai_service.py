import requests
import json
import os
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard
from challenges import CHALLENGES
from prompting import prompt_manager


class AIService:
    def __init__(self, llm_server_url: str = None):
        self.llm_server_url = llm_server_url or os.getenv("LLM_SERVER_URL", "http://localhost:8001")
        self.board_encoder = BoardEncoder()
        self.challenges = CHALLENGES
        print(f"[AIService] Using LLM server at: {self.llm_server_url}")

    def get_ai_move(self, board: GameBoard, challenge_id: str = None) -> Dict[str, Any]:
        try:
            game_state = {
                "components": self.board_encoder.encode_board(board),
                "marbles": [{"color": m.color, "x": m.x, "y": m.y} for m in board.marbles],
                "red_marbles": board.red_marbles,
                "blue_marbles": board.blue_marbles,
                "active_launcher": board.active_launcher
            }

            prompt = prompt_manager.generate_prompt('library', game_state, challenge_id)
            print("[DEBUG] Sending prompt to LLaMA:\n", prompt)

            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt, "max_tokens": 512, "temperature": 0.7},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"LLM server error: {response.text}")

            result = response.json()
            if "output" not in result:
                raise Exception("No valid 'output' field from LLM")

            return json.loads(result["output"])

        except requests.exceptions.Timeout:
            print("[AIService] Timeout! Server not responding.")
            raise Exception("LLM server timeout. Please try again.")
        except requests.exceptions.ConnectionError as e:
            print(f"[AIService] Connection error: {e}")
            raise Exception("LLM server not reachable. Is SSH tunnel active?")
        except Exception as e:
            print(f"[AIService] Unexpected error: {e}")
            raise

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any], challenge_id: str = None) -> str:
        try:
            game_state = {
                "components": self.board_encoder.encode_board(board),
                "marbles": [{"color": m.color, "x": m.x, "y": m.y} for m in board.marbles],
                "red_marbles": board.red_marbles,
                "blue_marbles": board.blue_marbles,
                "active_launcher": board.active_launcher
            }

            prompt = prompt_manager.generate_prompt('library', game_state, challenge_id)
            prompt += f"\n\nMove to explain: {json.dumps(move, indent=2)}"

            print("[DEBUG] Sending explanation prompt to LLaMA:\n", prompt)

            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt, "max_tokens": 512, "temperature": 0.7},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"LLM server error: {response.text}")

            result = response.json()
            return result["output"].strip()

        except requests.exceptions.Timeout:
            print("[AIService] Timeout! Server not responding.")
            raise Exception("LLM server timeout. Please try again.")
        except requests.exceptions.ConnectionError as e:
            print(f"[AIService] Connection error: {e}")
            raise Exception("LLM server not reachable. Is SSH tunnel active?")
        except Exception as e:
            print(f"[AIService] Unexpected error: {e}")
            raise