from mako.template import Template
from challenges import CHALLENGES
from board_encoder import BoardEncoder

def generate_ai_prompt(challenge_id: int):
    # Load the template
    template = Template(filename="TemplateLibrary.md")
    print(CHALLENGES.keys())

    # Get the challenge details
    challenge_key = str(challenge_id)  # Convert the challenge ID to a string
    challenge = CHALLENGES.get(challenge_key)  # Retrieve the challenge object
    if not challenge:
        raise ValueError(f"Challenge with ID {challenge_id} not found")

    print(f"Challenge details: {challenge}")  # Debugging

    # Prepare the challenge description for the prompt
    challenge_description = f"""
    Challenge: {challenge['id']}
    Board Layout: {BoardEncoder._encode_board_layout(challenge['board'])}
    """

    # Define dynamic values
    toolbox_code = """functions"""

    # Fill the template
    filled_prompt = template.render(
        toolbox=toolbox_code,
        question=challenge_description
    )
    print(filled_prompt)
    return filled_prompt
prompt = generate_ai_prompt(1)