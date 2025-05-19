import requests
import json
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard

class AIService:
    def __init__(self, llm_server_url: str = "http://localhost:8001"):
        self.llm_server_url = llm_server_url
        self.board_encoder = BoardEncoder()

    def get_ai_move(self, board: GameBoard, challenge_id: str = None) -> Dict[str, Any]:
        """Get AI move suggestion for the current board state."""
        try:
            # Encode the board state
            encoded_state = self.board_encoder.encode_board(board)
            
            # Get challenge context if challenge_id is provided
            challenge_context = ""
            if challenge_id:
                challenge = self.challenges.get_challenge(challenge_id)
                if challenge:
                    challenge_context = f"\nChallenge Context:\n{challenge.description}\n"
            
            # Construct a strict prompt that enforces JSON output
            prompt = f"""
You are an expert Turing Tumble assistant. Your task is to suggest the best next move based on the board state.

{challenge_context}

Turing Tumble Game State:
{encoded_state}

IMPORTANT:
- Respond ONLY with a VALID JSON object.
- DO NOT include any explanation before or after the JSON.
- DO NOT use markdown, bullet points, or tags.

Valid format:
{{
  "action": "add_component",  # or "launch_marble" or "set_launcher"
  "parameters": {{
    "type": "ramp_left",      # if applicable
    "x": 3,
    "y": 5
  }},
  "explanation": "A ramp at (3, 5) helps guide the marble left."
}}

Output this JSON object directly, and nothing else.
"""
            
            print("[AIService] Prompt sent to LLaMA:\n", prompt)
            
            # Get response from LLM using direct HTTP request
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
            
            # Get the move from the response
            move = llm_response["response"]
            
            # Force stringify if already parsed
            if isinstance(move, dict):
                move = json.dumps(move)
            
            # Try to parse the move as JSON
            try:
                move = json.loads(move)
            except json.JSONDecodeError:
                print("[AIService] ERROR: Could not parse move as JSON.")
                raise ValueError("Invalid JSON format in move")
            
            # Validate move structure
            if not isinstance(move, dict):
                print("[AIService] ERROR: Move is not a dictionary.")
                raise ValueError("Invalid move format: expected dictionary")
                
            if "action" not in move:
                print("[AIService] ERROR: Move missing 'action' field.")
                raise ValueError("Invalid move format: missing 'action' field")
                
            return move
            
        except Exception as e:
            print(f"[AIService] Error getting AI move: {str(e)}")
            raise

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any], challenge_id: str = None) -> str:
        """
        Get AI's explanation for a specific move in the context of a challenge.
        """
        encoded_state = self.board_encoder.encode_board(board)

        # Add challenge context to explanation request
        challenge_context = ""
        if challenge_id:
            if challenge_id == "1":
                challenge_context = "\nThis move is part of Challenge 1: Gravity, where we need to guide all blue marbles to the end."
            elif challenge_id == "2":
                challenge_context = "\nThis move is part of Challenge 2: Re-Entry, where we need to create a path for blue marbles to re-enter."

        prompt = f"""Explain why the following move is a good strategic choice in the Turing Tumble game.

Game State:
{encoded_state}

Move:
{str(move)}
{challenge_context}

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
