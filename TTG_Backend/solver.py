import os
import re
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from .game_logic import GameBoard, ComponentType, BLUE
from .board_encoder import BoardEncoder
from .AIChallengeSolver import TransformerPlanner

# Set device to CUDA if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# AI Planner powered by GPT-2 for generating move plans
class TransformerPlanner:
    def __init__(self, model_path=None):
        print("Initializing the AI planner using GPT-2...")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        if model_path and os.path.exists(model_path):
            print(f"Loading fine-tuned model from: {model_path}")
            self.model = GPT2LMHeadModel.from_pretrained(model_path)
        else:
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        
        # Move model to appropriate device
        self.model = self.model.to(device)
        print(f"Model loaded on {device}")

    def plan(self, input_text: str):
        print("Generating plan from board state...")
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to(device)
        output = self.model.generate(input_ids, max_length=50, num_return_sequences=1)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def parse_plan(self, plan_text: str):
        print("Parsing generated plan...")
        pattern = r"(RAMP_LEFT|RAMP_RIGHT) at \((\d+), (\d+)\)"
        matches = re.findall(pattern, plan_text)
        steps = []
        for direction, x, y in matches:
            comp_type = ComponentType[direction]  # Convert text to ComponentType enum
            steps.append((comp_type, int(x), int(y)))
        return steps

def setup_challenge() -> GameBoard:
    board = GameBoard()  # Default 15x17 size
    print("Setting up the puzzle board...")
    
    # Add some test components
    board.set_component(7, 5, ComponentType.RAMP_LEFT)
    board.set_component(7, 7, ComponentType.RAMP_RIGHT)
    board.set_component(7, 3, ComponentType.CROSSOVER)
    board.set_component(6, 4, ComponentType.INTERCEPTOR)
    
    return board

def run_solver():
    try:
        print("Starting solver...")
        # Create and setup the board
        board = setup_challenge()
        print("Board created successfully")
        
        # Create board encoder
        encoder = BoardEncoder()
        print("Encoder created successfully")
        
        # Encode and print the board state
        print("\nInitial Board State:")
        board.print_board()
        
        print("\nEncoded Board State:")
        encoded_text = encoder.encode_board(board)
        print(encoded_text)
        
        # Drop a blue marble
        print("\nDropping a blue marble...")
        board.drop_marble(7, BLUE)
        
        print("\nBoard State After Marble Drop:")
        board.print_board()
        
        print("\nMarble Outputs:")
        print(f"Blue marble outputs: {board.outputs[BLUE]}")
        
        print("\nGame Rules:")
        print(encoder.encode_game_rules())
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

def solve_challenge(challenge_id: str) -> dict:
    """Solve a specific challenge using the AI solver"""
    # Initialize components
    board = GameBoard()
    encoder = BoardEncoder()
    planner = TransformerPlanner()
    
    # Get the encoded state
    encoded_state = encoder.encode_board(board)
    
    # Generate solution plan
    plan = planner.plan(encoded_state)
    steps = planner.parse_plan(plan)
    
    return {
        'plan': plan,
        'steps': steps
    }

if __name__ == '__main__':
    print("Script started")
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("Number of GPUs:", torch.cuda.device_count())
        print("GPU Name:", torch.cuda.get_device_name(0))
    else:
        print("Running on CPU mode")
    run_solver()
    print("Script completed") 