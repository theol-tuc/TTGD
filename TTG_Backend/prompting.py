from mako.template import Template
from challenges import CHALLENGES
from board_encoder import BoardEncoder

def generate_ai_prompt(challenge_id: str):
    # Load the template
    template = Template(filename="TemplateLibrary.md")

    # Get the challenge details
    challenge = CHALLENGES.get(challenge_id)
    if not challenge:
        raise ValueError(f"Challenge with ID {challenge_id} not found")

    # Prepare the challenge description for the prompt
    challenge_description = f"""
    Challenge: {challenge['name']}
    Description: {challenge['description']}
    Board Layout: {BoardEncoder._encode_board_layout(challenge['board'])}
    """

    # Define dynamic values
    toolbox_code = """functions"""

    # Fill the template
    filled_prompt = template.render(
        toolbox=toolbox_code,
        question=challenge_description
    )
    print(filled_prompt.len())
    return filled_prompt
prompt = generate_ai_prompt(1)