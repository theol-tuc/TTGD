import requests
import json
import os
import re
from typing import Dict, Any, Optional, List
from board_encoder import BoardEncoder
from game_logic import GameBoard
from challenges import CHALLENGES
from prompting import prompt_manager, extract_json_from_response

def parse_ai_component_calls(calls: List[str]) -> List[Dict[str, Any]]:
    """
    Parse strings like: "add_component(type=ItemType.RampLeft, x=4, y=0)"
    into structured objects: {"type": "RampLeft", "x": 4, "y": 0}
    """
    parsed = []
    for call in calls:
        match = re.match(r'add_component\(type=ItemType\.(\w+), x=(\d+), y=(\d+)\)', call)
        if match:
            comp_type, x, y = match.groups()
            parsed.append({
                "type": comp_type,
                "x": int(x),
                "y": int(y)
            })
        else:
            print(f"Warning: Could not parse AI command: {call}")
    return parsed

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
                json={"prompt": prompt, "max_tokens": 512, "temperature": 0.4},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"LLM server error: {response.text}")

            result = response.json()
            if "output" not in result:
                raise Exception("No valid 'output' field from LLM")

            # Extract clean JSON from response
            raw_output = result["output"]
            clean_json = extract_json_from_response(raw_output)
            print(f"[DEBUG] Raw output: {raw_output}")
            print(f"[DEBUG] Cleaned JSON: {clean_json}")

            # Check for empty or invalid JSON before parsing
            if not clean_json.strip():
                raise ValueError(f"LLM returned empty response. Raw output: {repr(raw_output)}")
            
            if not clean_json.strip().startswith("["):
                raise ValueError(f"Cleaned output is not valid JSON array. Output: {repr(clean_json)}")

            # Parse the JSON and convert string commands to structured objects
            json_list = json.loads(clean_json)
            parsed_components = parse_ai_component_calls(json_list)
            print(f"[DEBUG] Parsed components: {parsed_components}")

            # Validate that we got valid component instructions
            if not parsed_components:
                raise ValueError("LLM did not return any valid component instructions. Raw output: " + raw_output[:200])

            # Return in the format expected by the frontend
            if parsed_components:
                # Take the first component as the main action
                first_component = parsed_components[0]
                return {
                    "action": "add_component",
                    "parameters": {
                        "type": first_component["type"],
                        "x": first_component["x"],
                        "y": first_component["y"],
                        "all_components": parsed_components  # Include all components for reference
                    },
                    "explanation": f"AI suggests adding {len(parsed_components)} component(s) to solve the challenge. First component: {first_component['type']} at position ({first_component['x']}, {first_component['y']})."
                }
            else:
                return {
                    "action": "no_action",
                    "parameters": {},
                    "explanation": "AI could not determine a valid move."
                }

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