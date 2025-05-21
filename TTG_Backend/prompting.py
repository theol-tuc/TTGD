from mako.template import Template
from challenges import CHALLENGES
from board_encoder import BoardEncoder
from typing import Dict, Any, Optional

class PromptManager:
    def __init__(self):
        self.templates = {
            'matrix': Template(filename="TemplateMatrix.md"),
            'library': Template(filename="TemplateLibrary.md"),
            'analysis': Template(filename="TemplateAna.md")
        }
        self.board_encoder = BoardEncoder()

    def _get_challenge_context(self, challenge_id: str) -> Dict[str, Any]:
        """Get formatted challenge information."""
        challenge = CHALLENGES.get(str(challenge_id))
        if not challenge:
            raise ValueError(f"Challenge with ID {challenge_id} not found")
        
        return {
            'id': challenge['id'],
            'description': challenge['description'],
            'available_parts': challenge['availableParts'],
            'board_layout': self.board_encoder._encode_board_layout(challenge['board']),
            'red_marbles': challenge['red_marbles'],
            'blue_marbles': challenge['blue_marbles'],
            'expected_output': challenge['expectedOutput']
        }

    def _format_challenge_description(self, context: Dict[str, Any]) -> str:
        """Format challenge information into a description string."""
        return f"""
        Challenge: {context['id']}
        Description: {context['description']}
        Available Parts: {context['available_parts']}
        Board Layout:
{context['board_layout']}
        Red Marbles: {context['red_marbles']}
        Blue Marbles: {context['blue_marbles']}
        Expected Output: {context['expected_output']}
        """

    def generate_prompt(self, 
                       context_type: str, 
                       game_state: Dict[str, Any], 
                       challenge_id: Optional[str] = None) -> str:
        """
        Generate a prompt based on the context type and game state.
        
        Args:
            context_type: One of 'matrix', 'library', or 'analysis'
            game_state: Current game state
            challenge_id: Optional challenge ID for challenge-specific prompts
        """
        if context_type not in self.templates:
            raise ValueError(f"Invalid context type: {context_type}")

        template = self.templates[context_type]
        
        # Prepare context data
        context = {
            'board_state': self.board_encoder.encode_board(game_state),
            'toolbox': self._get_toolbox_functions(context_type)
        }

        # Add challenge context if available
        if challenge_id:
            challenge_context = self._get_challenge_context(challenge_id)
            context['question'] = self._format_challenge_description(challenge_context)
            context['challenge'] = challenge_context

        return template.render(**context)

    def _get_toolbox_functions(self, context_type: str) -> str:
        """Get the appropriate toolbox functions based on context type."""
        if context_type == 'matrix':
            return """
            def initialize_board(self) -> None:
                \"\"\"Initialize the board with empty components\"\"\"
                self.components = [[Component(ComponentType.EMPTY, x, y)
                                for x in range(self.width)]
                               for y in range(self.height)]
            """
        elif context_type == 'library':
            return """
            def add_component(self, type: ComponentType, x: int, y: int) -> None:
                \"\"\"Adds a component to the board at (x, y) if within bounds.\"\"\"
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.components[y][x] = Component(type, x, y)
            """
        return ""

# Create a singleton instance
prompt_manager = PromptManager()

def generate_ai_prompt(challenge_id: int = None, game_state: Dict[str, Any] = None) -> str:
    """
    Generate an AI prompt based on the context.
    If challenge_id is provided, generates a challenge-specific prompt.
    Otherwise, generates a general gameplay prompt.
    """
    if challenge_id:
        return prompt_manager.generate_prompt('library', game_state, str(challenge_id))
    return prompt_manager.generate_prompt('matrix', game_state)

prompt = generate_ai_prompt(1)