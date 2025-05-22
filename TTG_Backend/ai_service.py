import requests
import json
import os
import random
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
        self.use_dummy_ai = os.getenv("USE_DUMMY_AI", "0") == "1"
        print(f"[AIService] Using LLM server at: {self.llm_server_url}")
        if self.use_dummy_ai:
            print("[AIService] Running in DUMMY AI mode - will return test responses")

    def _get_dummy_move(self) -> Dict[str, Any]:
        """Return a random dummy move for testing."""
        actions = [
            {
                "action": "place_component",
                "parameters": {
                    "type": "gear",
                    "x": random.randint(0, 7),
                    "y": random.randint(0, 7),
                    "rotation": 0
                },
                "explanation": "Placing a gear to connect components."
            },
            {
                "action": "place_component",
                "parameters": {
                    "type": "crossover",
                    "x": random.randint(0, 7),
                    "y": random.randint(0, 7),
                    "rotation": 0
                },
                "explanation": "Placing a crossover to allow bi-directional ball movement."
            },
            {
                "action": "place_marble",
                "parameters": {
                    "color": random.choice(["red", "blue"]),
                    "x": random.randint(0, 7),
                    "y": random.randint(0, 7)
                },
                "explanation": "Placing a marble to simulate the start of the game."
            },
            {
                "action": "rotate_component",
                "parameters": {
                    "x": random.randint(0, 7),
                    "y": random.randint(0, 7),
                    "rotation": random.choice([0, 90, 180, 270])
                },
                "explanation": "Rotating a component to redirect marbles."
            }
        ]
        return random.choice(actions)

    def _get_dummy_explanation(self, move: Dict[str, Any]) -> str:
        """Return a dummy explanation based on the move."""
        action = move.get("action", "unknown")
        params = move.get("parameters", {})
        return f"Dummy explanation for {action} with parameters: {json.dumps(params)}"

    def get_ai_move(self, board: GameBoard, challenge_id: str = None) -> Dict[str, Any]:
        if self.use_dummy_ai:
            print("[AIService] Dummy mode: returning dummy move.")
            return self._get_dummy_move()

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
                json={"prompt": prompt},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"LLM server error: {response.text}")

            result = response.json()
            if "response" not in result:
                raise Exception("No valid 'response' field from LLM")

            return result["response"]

        except requests.exceptions.Timeout:
            print("[AIService] Timeout! Falling back to dummy move.")
            return self._get_dummy_move()
        except requests.exceptions.ConnectionError as e:
            print(f"[AIService] Connection error: {e}")
            raise Exception("LLM server not reachable. Is SSH tunnel active?")
        except Exception as e:
            print(f"[AIService] Unexpected error: {e}")
            if self.use_dummy_ai:
                return self._get_dummy_move()
            raise

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any], challenge_id: str = None) -> str:
        if self.use_dummy_ai:
            print("[AIService] Dummy mode: returning dummy explanation.")
            return self._get_dummy_explanation(move)

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
                json={"prompt": prompt},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"LLM server error: {response.text}")

            result = response.json()
            return result["response"].get("explanation", "No explanation provided")

        except requests.exceptions.Timeout:
            print("[AIService] Timeout! Falling back to dummy explanation.")
            return self._get_dummy_explanation(move)
        except requests.exceptions.ConnectionError as e:
            print(f"[AIService] Connection error: {e}")
            raise Exception("LLM server not reachable. Is SSH tunnel active?")
        except Exception as e:
            print(f"[AIService] Unexpected error: {e}")
            if self.use_dummy_ai:
                return self._get_dummy_explanation(move)
            raise