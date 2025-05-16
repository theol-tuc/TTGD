# AI Challenge Solver using a fine-tuned GPT-2 and symbolic board planner

import os
import re
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from TTG_Backend.game_logic import GameBoard, ComponentType, BLUE
from TTG_Backend.board_encoder import BoardEncoder

# AI Planner powered by GPT-2 for generating move plans
class TransformerPlanner:
    def __init__(self, model_path=None):
        print("Initializing the AI planner using GPT-2...")
        local_gpt2_path = "TTG_Backend/models/gpt2"
        if model_path and os.path.exists(model_path):
            print(f"Loading fine-tuned model from: {model_path}")
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            self.model = GPT2LMHeadModel.from_pretrained(model_path)
        elif os.path.exists(local_gpt2_path):
            print(f"Loading GPT-2 from local path: {local_gpt2_path}")
            self.tokenizer = GPT2Tokenizer.from_pretrained(local_gpt2_path)
            self.model = GPT2LMHeadModel.from_pretrained(local_gpt2_path)
        else:
            self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")

    def plan(self, input_text: str):
        print("Generating plan from board state...")
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
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

# Optional: Train GPT-2 on example board-plan pairs
def fine_tune_model(train_file: str, output_dir: str, epochs=3):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    dataset = TextDataset(tokenizer=tokenizer, file_path=train_file, block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=2,
        save_steps=5000,
        save_total_limit=2,
        logging_dir=os.path.join(output_dir, 'logs')
    )

    trainer = Trainer(model=model, args=training_args, data_collator=data_collator, train_dataset=dataset)
    print("Starting fine-tuning process...")
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Model fine-tuning complete. Saved to:", output_dir)

# Define a simple challenge board layout
def setup_challenge() -> GameBoard:
    board = GameBoard()  # Default 15x17 size
    print("Setting up the puzzle board...")
    
    # Add some test components
    board.set_component(7, 5, ComponentType.RAMP_LEFT)
    board.set_component(7, 7, ComponentType.RAMP_RIGHT)
    board.set_component(7, 3, ComponentType.CROSSOVER)
    board.set_component(6, 4, ComponentType.INTERCEPTOR)
    
    return board

# Run the AI Solver: Encode board → Plan moves → Apply → Simulate
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

if __name__ == '__main__':
    print("Script started")
    print("CUDA available:", torch.cuda.is_available())
    print("Number of GPUs:", torch.cuda.device_count())
    if torch.cuda.is_available():
        print("GPU Name:", torch.cuda.get_device_name(0))
    print("Using device:", torch.cuda.current_device())
    run_solver()
    print("Script completed")
