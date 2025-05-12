import random
from typing import Dict, Any, Optional

class AIManager:
    def __init__(self):
        self.possible_components = ["ramp", "gear", "bit", "crossover", "interceptor"]
        self.possible_actions = ["add_component", "launch_marble", "set_launcher"]

    def get_ai_move(self, game_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get AI's next move based on the current game state"""
        try:
            # Randomly choose an action
            action = random.choice(self.possible_actions)
            
            if action == "add_component":
                # Find an empty spot on the board
                empty_spots = []
                for y in range(len(game_state['components'])):
                    for x in range(len(game_state['components'][y])):
                        if not game_state['components'][y][x]['is_occupied']:
                            empty_spots.append((x, y))
                
                if empty_spots:
                    x, y = random.choice(empty_spots)
                    return {
                        "action": "add_component",
                        "parameters": {
                            "type": random.choice(self.possible_components),
                            "x": x,
                            "y": y
                        }
                    }
            
            elif action == "launch_marble":
                return {
                    "action": "launch_marble",
                    "parameters": {
                        "color": random.choice(["red", "blue"])
                    }
                }
            
            elif action == "set_launcher":
                return {
                    "action": "set_launcher",
                    "parameters": {
                        "launcher": random.choice(["left", "right"])
                    }
                }
            
            return None
            
        except Exception as e:
            print(f"Error in get_ai_move: {e}")
            return None

    def get_ai_explanation(self, game_state: Dict[str, Any], move: Dict[str, Any]) -> str:
        """Get AI's explanation for its move"""
        try:
            action = move["action"]
            params = move["parameters"]
            
            if action == "add_component":
                return f"Adding a {params['type']} at position ({params['x']}, {params['y']}) to create a new path for marbles."
            elif action == "launch_marble":
                return f"Launching a {params['color']} marble to test the current board configuration."
            elif action == "set_launcher":
                return f"Setting the active launcher to {params['launcher']} to try a different starting position."
            else:
                return "Making a strategic move to improve the board configuration."
            
        except Exception as e:
            print(f"Error in get_ai_explanation: {e}")
            return "Making a strategic move to improve the board configuration." 