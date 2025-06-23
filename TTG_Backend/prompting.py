from mako.template import Template
from typing import Dict, Any, Optional
import os
from challenges import CHALLENGES
from board_encoder import BoardEncoder
import json
import re

def extract_json_from_response(response_text):
    """
    Extract JSON array from the model response, removing any explanatory text.
    """
    # Try to find JSON array pattern
    json_match = re.search(r"\[\s*\"add_component.*?\]", response_text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # Safety net: find the last complete JSON array
    end_index = response_text.rfind("]")
    if end_index != -1:
        start_index = response_text.rfind("[", 0, end_index + 1)
        if start_index != -1:
            return response_text[start_index:end_index + 1]
    
    # If no match found, return the original response
    return response_text

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
        
        # Add challenge context if provided
        challenge_context = ""
        if challenge_id and challenge_id in CHALLENGES:
            challenge = CHALLENGES[challenge_id]
            try:
                board_layout = BoardEncoder._encode_board_layout(challenge['board'])
                challenge_context = f"""
Challenge Description:
{challenge.get('description', 'No description available')}

Objective:
{challenge.get('objective', 'No objective specified')}

Available Parts:
{challenge.get('availableParts', 'No parts specified')}

Board Layout:
{board_layout}

Expected Output:
{challenge.get('expectedOutput', 'No expected output specified')}
"""
            except Exception as e:
                print(f"Error encoding challenge board: {str(e)}")
                challenge_context = f"""
Challenge Description:
{challenge.get('description', 'No description available')}

Objective:
{challenge.get('objective', 'No objective specified')}

[Error: Could not encode board layout]
"""
        
        # Force JSON-only output with strict instructions and length limit
        prompt = f"""Only return a JSON list of at most 4 add_component function calls.
Do NOT write any explanations, comments, functions, or extra output.
The format must be:

[
  "add_component(type=ItemType.RampLeft, x=6, y=6)",
  "add_component(type=ItemType.RampLeft, x=8, y=6)"
]

Your response must start with [ and end with ].
If you return anything else, it will crash the game.
Now solve the following challenge:

Game State:
{json.dumps(game_state)}

{challenge_context}

Remember: ONLY return the JSON list with at most 4 components. Nothing else."""
        
        return prompt

# Create a singleton instance
prompt_manager = PromptManager()