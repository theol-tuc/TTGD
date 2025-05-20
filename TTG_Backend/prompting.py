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
    toolbox_code = """    
    
    def initialize_board(self) -> None:
        \"\"\"Initialize the board with empty components\"\"\"
        self.components = [[Component(ComponentType.EMPTY, x, y)
                            for x in range(self.width)]
                           for y in range(self.height)]

        # Set up borders and invalid spaces
        self.setup_board_structure()

    def setup_board_structure(self) -> None:
        \"\"\"Set up the board structure with borders and invalid spaces\"\"\"

        #Set up the diamond pattern
        self.setup_diamond_pattern()

        # Set vertical borders
        for y in range(self.height):
            self.components[y][0].type = ComponentType.BORDER_VERTICAL
            self.components[y][14].type = ComponentType.BORDER_VERTICAL

        # Set horizontal border (last row)
        for x in range(self.width):
            self.components[16][x].type = ComponentType.BORDER_HORIZONTAL

        # Add levers at the bottom
        self.components[14][6].type = ComponentType.LEVER_BLUE
        self.components[14][5].type = ComponentType.LEVER_BLUE
        self.components[14][3].type = ComponentType.LEVER_BLUE
        self.components[14][8].type = ComponentType.LEVER_RED
        self.components[14][9].type = ComponentType.LEVER_RED
        self.components[14][11].type = ComponentType.LEVER_RED

        # Add corners
        self.components[16][0].type = ComponentType.CORNER_LEFT
        self.components[16][14].type = ComponentType.CORNER_RIGHT

        # Add launchers at the top
        self.components[2][5].type = ComponentType.LAUNCHER  # Left launcher
        self.components[2][9].type = ComponentType.LAUNCHER  # Right launcher

        for y in range (1, self.width-1):
            self.components[13][y].type = ComponentType.INVALID

        self.components[13][7].type = ComponentType.EMPTY
        self.components[14][7].type = ComponentType.INVALID
        self.components[15][7].type = ComponentType.INVALID

    def setup_diamond_pattern(self) -> None:
        \"\"\"Set up the diamond pattern of invalid spaces\"\"\"
        # Row 1 (index 0)
        for x in range(1, self.width - 1):
            if x == 1 or (3 <= x <= 11) or x == 13:
                self.components[0][x].type = ComponentType.INVALID
            elif x == 2:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 12:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 2 (index 1)
        for x in range(1, self.width - 1):
            if x in [1, 2] or (4 <= x <= 10) or x in [12, 13]:
                self.components[1][x].type = ComponentType.INVALID
            elif x == 3:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 11:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 3 (index 2)
        for x in range(1, self.width - 1):
            if x in [1, 2, 3] or (5 <= x <= 9) or x in [11, 12, 13]:
                self.components[2][x].type = ComponentType.INVALID
            elif x == 4:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 10:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 4 (index 3)
        for x in range(1, self.width - 1):
            if x in [1,2,3,7,11,12,13]:
                self.components[3][x].type = ComponentType.INVALID
            elif x % 2 == 0:
                self.components[3][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[3][x].type = ComponentType.EMPTY

        # Row 5 (index 4)
        for x in range(1, self.width):
            if x in [1,2,12,13]:
                self.components[4][x].type = ComponentType.INVALID
            elif x % 2 == 1:
                self.components[4][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[4][x].type = ComponentType.EMPTY



        # Middle rows
        for y in range(5, 13):
            for x in range(2,14):
                if (x + y) % 2 == 1:
                    self.components[y][x].type = ComponentType.GRAY_SPACE
                else:
                    self.components[y][x].type = ComponentType.EMPTY
            self.components[y][1].type = ComponentType.INVALID
            self.components[y][13].type = ComponentType.INVALID

        # Bottom rows
        for y in range(self.height - 3, self.height - 1):
            for x in range(1, self.width - 1):
                if (x <= 6) or (x >= 8):
                    self.components[y][x].type = ComponentType.INVALID

        self.components[14][6].type = ComponentType.LEVER_BLUE
        self.components[14][5].type = ComponentType.LEVER_BLUE
        self.components[14][3].type = ComponentType.LEVER_BLUE
        self.components[14][8].type = ComponentType.LEVER_RED
        self.components[14][9].type = ComponentType.LEVER_RED
        self.components[14][11].type = ComponentType.LEVER_RED"""

    # Fill the template
    filled_prompt = template.render(
        toolbox=toolbox_code,
        question=challenge_description
    )
    print(filled_prompt)
    return filled_prompt
prompt = generate_ai_prompt(2)