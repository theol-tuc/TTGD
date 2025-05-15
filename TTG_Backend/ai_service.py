import requests
from typing import Dict, Any, Optional
from board_encoder import BoardEncoder
from game_logic import GameBoard

class AIService:
    def __init__(self, llm_server_url: str = "http://cloud-247.rz.tu-clausthal.de:8001"):
        self.llm_server_url = llm_server_url
        self.board_encoder = BoardEncoder()

    def get_ai_move(self, board: GameBoard) -> Dict[str, Any]:
        """
        Get AI's next move based on current board state
        Returns a dictionary with action and parameters
        """
        # Encode board state
        encoded_state = self.board_encoder.encode_board(board)
        
        # Prepare prompt for LLM
        prompt = f"""Given the following Turing Tumble game state, suggest the next best move:

{encoded_state}

Please respond in the following JSON format:
{{
    "action": "add_component|launch_marble|set_launcher",
    "parameters": {{
        // For add_component: "type": "GEAR|BIT_LEFT|BIT_RIGHT|RAMP_LEFT|RAMP_RIGHT|CROSSOVER|INTERCEPTOR",
        //                     "x": number, "y": number
        // For launch_marble: "color": "red|blue"
        // For set_launcher: "launcher": "left|right"
    }},
    "explanation": "Brief explanation of why this move is suggested"
}}"""

        try:
            # Send to LLM server
            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            
            # Parse LLM response
            llm_response = response.json()
            move = llm_response["response"]
            
            return move
            
        except Exception as e:
            print(f"Error getting AI move: {str(e)}")
            return {
                "action": "launch_marble",
                "parameters": {"color": "red"},
                "explanation": "Error getting AI move, defaulting to launching a red marble"
            }

    def get_ai_explanation(self, board: GameBoard, move: Dict[str, Any]) -> str:
        """
        Get AI's explanation for a specific move
        """
        encoded_state = self.board_encoder.encode_board(board)
        
        prompt = f"""Given the following Turing Tumble game state and move:

State:
{encoded_state}

Move:
{str(move)}

Please explain why this move is a good choice and what it accomplishes."""

        try:
            response = requests.post(
                f"{self.llm_server_url}/generate",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            
            return response.json()["response"]
            
        except Exception as e:
            return f"Error getting AI explanation: {str(e)}" 