import requests
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard

class AIService:
    def __init__(self, llm_server_url: str = "http://localhost:8001"):
        self.llm_server_url = llm_server_url
        self.board_encoder = BoardEncoder()

    def get_ai_move(self, board: GameBoard) -> Dict[str, Any]:
        """
        Get AI's next move based on current board state.
        Returns a dictionary with action and parameters.
        """
        encoded_state = self.board_encoder.encode_board(board)

        prompt = f"""You are an expert Turing Tumble assistant. Given the board state below, suggest the optimal next move.

Turing Tumble Game State:
{encoded_state}

Respond ONLY with a valid JSON object using the format below.
Do NOT include any commentary, text, or explanation outside the JSON.
Do NOT write markdown or tags.

Example format:
{{
  "action": "launch_marble",
  "parameters": {{
    "color": "red"
  }},
  "explanation": "Launching a red marble will trigger the current setup and allow progress."
}}

Valid actions:
- "add_component"
- "launch_marble"
- "set_launcher"

Return ONLY the JSON object.
"""

        print("[AIService] Prompt sent to LLaMA:\n", prompt)

        try:
            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt}
            )

            print("[AIService] Raw response from LLaMA:\n", response.text)
            response.raise_for_status()

            llm_response = response.json()
            if "response" not in llm_response:
                print("[AIService] ERROR: 'response' key missing in LLaMA output.")
                raise ValueError("Missing 'response' in LLaMA output")

            move = llm_response["response"]
            print("[AIService] Parsed LLaMA move:\n", move)
            return move

        except Exception as e:
            print(f"[AIService] Error getting AI move: {str(e)}")
            return {
                "action": "launch_marble",
                "parameters": {"color": "red"},
                "explanation": "Error getting AI move, defaulting to launching a red marble"
            }

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any]) -> str:
        """
        Get AI's explanation for a specific move.
        """
        encoded_state = self.board_encoder.encode_board(board)

        prompt = f"""Explain why the following move is a good strategic choice in the Turing Tumble game.

Game State:
{encoded_state}

Move:
{str(move)}

Respond with a clear, concise explanation. Do not include formatting or tags.
"""

        print("[AIService] Prompt for explanation:\n", prompt)

        try:
            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt}
            )

            print("[AIService] Raw explanation response:\n", response.text)
            response.raise_for_status()

            response_json = response.json()
            if "response" not in response_json:
                print("[AIService] ERROR: 'response' key missing in explanation output.")
                return "Error: LLaMA response did not include explanation."

            return response_json["response"]

        except Exception as e:
            print(f"[AIService] Error getting explanation: {str(e)}")
            return "Error getting AI explanation."
