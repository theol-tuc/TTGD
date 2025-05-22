from mako.template import Template
from typing import Dict, Any, Optional
import os
from challenges import CHALLENGES
from board_encoder import BoardEncoder
import json

class PromptManager:
    def __init__(self):
        self.templates = {
            'library': self._load_template('TemplateLibrary.md'),
            'matrix': self._load_template('TemplateMatrix.md'),
            'analysis': self._load_template('TemplateAna.md')
        }

    def _load_template(self, filename: str) -> str:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading template {filename}: {str(e)}")
            return ""

    def generate_prompt(self, template_type: str, game_state: Dict[str, Any], challenge_id: Optional[str] = None) -> str:
        """
        Generate a prompt using the specified template type and game state.
        """
        template = self.templates.get(template_type, self.templates['library'])
        
        # Add JSON format instructions
        json_format = """
You must respond with a valid JSON object in the following format:
{
    "action": "place_component" | "rotate_component" | "place_marble" | "remove_component",
    "parameters": {
        // Parameters specific to the action
        // For place_component: "type", "x", "y", "rotation"
        // For rotate_component: "x", "y", "rotation"
        // For place_marble: "color", "x", "y"
        // For remove_component: "x", "y"
    },
    "explanation": "Your detailed explanation of the move"
}

IMPORTANT: Wrap your response in [START_JSON] and [END_JSON] tags.
Example:
[START_JSON]
{
    "action": "place_component",
    "parameters": {
        "type": "gear",
        "x": 3,
        "y": 2,
        "rotation": 0
    },
    "explanation": "I am placing a gear at position (3,2) to..."
}
[END_JSON]
"""
        
        # Add challenge context if provided
        challenge_context = ""
        if challenge_id and challenge_id in CHALLENGES:
            challenge = CHALLENGES[challenge_id]
            try:
                # Directly use the board object, not a dict
                board_layout = BoardEncoder._encode_board_layout(challenge['board'])
                challenge_context = f"""
Current Challenge ID: {challenge_id}
Description: {challenge.get('description', 'No description available')}
Objective: {challenge.get('objective', 'No objective specified')}
Available Parts: {challenge.get('availableParts', 'No parts specified')}
Board Layout:
{board_layout}
Red Marbles: {challenge.get('red_marbles', 0)}
Blue Marbles: {challenge.get('blue_marbles', 0)}
Expected Output: {challenge.get('expectedOutput', 'No expected output specified')}
"""
            except Exception as e:
                print(f"Error encoding challenge board: {str(e)}")
                challenge_context = f"""
Current Challenge ID: {challenge_id}
Description: {challenge.get('description', 'No description available')}
Objective: {challenge.get('objective', 'No objective specified')}
[Error: Could not encode board layout]
"""
        
        # Format the prompt
        prompt = f"""
{template}

{challenge_context}

Current Game State:
{json.dumps(game_state, indent=2)}

{json_format}

Please analyze the current state and provide your next move in the specified JSON format.
"""
        
        return prompt

# Create a singleton instance
prompt_manager = PromptManager()