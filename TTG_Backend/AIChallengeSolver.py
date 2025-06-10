# AI-based puzzle solver using fine-tuned models for Turing Tumble challenges
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from typing import List, Dict, Optional
import numpy as np
from .game_logic import GameBoard, ComponentType, BLUE, RED
from .TuringTumble import TransformerPlanner

# Main solver class using fine-tuned GPT-2 for puzzle solving
class AIChallengeSolver:
    def __init__(self, model_path: Optional[str] = None):
        # Initialize the GPT-2 model and tokenizer for puzzle solving
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        
        # Load fine-tuned weights if provided
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Initialize game board for puzzle solving
        self.board = GameBoard()
        
        # Track solution steps for analysis
        self.solution_steps = []
        
        # Track success rate metrics
        self.success_count = 0
        self.total_attempts = 0
        
        # Initialize TransformerPlanner for enhanced planning
        self.planner = TransformerPlanner()

    # Convert board state to model input format
    def prepare_input(self, board_state: np.ndarray) -> torch.Tensor:
        # Flatten board state and convert to tensor for model input
        flattened = board_state.flatten()
        return torch.tensor(flattened, dtype=torch.float32)

    # Generate next move based on current board state
    def generate_move(self, board_state: np.ndarray) -> Dict:
        with torch.no_grad():
            # Prepare input tensor
            input_tensor = self.prepare_input(board_state)
            
            # Generate prediction using model
            outputs = self.model(input_tensor.unsqueeze(0))
            
            # Process output to get move
            move = self._process_model_output(outputs)
            
            # Use TransformerPlanner to enhance the move
            symbolic_output = self.planner.generate_plan(outputs.logits)
            move['plan'] = symbolic_output
            
            return move

    # Process model output to extract move information
    def _process_model_output(self, outputs) -> Dict:
        # Convert model logits to probabilities
        probs = torch.softmax(outputs.logits, dim=-1)
        
        # Get most likely move from probabilities
        move_idx = torch.argmax(probs).item()
        
        # Convert index to move format (position and color)
        return {
            'type': 'drop_marble',
            'position': move_idx % self.board.width,
            'color': BLUE if move_idx < self.board.width else RED
        }

    # Solve a specific challenge using the AI model
    def solve_challenge(self, challenge_config: Dict) -> List[Dict]:
        # Clear board for new challenge
        self.board.clear()
        
        # Set up challenge configuration
        self._setup_challenge(challenge_config)
        
        # Initialize solution tracking
        self.solution_steps = []
        
        # Set maximum attempts to prevent infinite loops
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            # Get current board state
            current_state = self.board.get_board_state()
            
            # Generate and apply next move
            move = self.generate_move(current_state)
            self._apply_move(move)
            
            # Record solution step
            self.solution_steps.append(move)
            
            # Check if challenge is solved
            if self._check_solution(challenge_config):
                self.success_count += 1
                break
            
            attempts += 1
        
        self.total_attempts += 1
        return self.solution_steps

    # Set up the board according to challenge configuration
    def _setup_challenge(self, config: Dict) -> None:
        # Configure number of marbles for the challenge
        self.board.set_number_of_marbles(
            config.get('red_marbles', 0),
            config.get('blue_marbles', 0)
        )
        
        # Place initial components on the board
        for comp in config.get('components', []):
            self.board.add_component(
                ComponentType[comp['type']],
                comp['x'],
                comp['y']
            )

    # Apply a move to the board
    def _apply_move(self, move: Dict) -> None:
        # Handle marble drops
        if move['type'] == 'drop_marble':
            self.board.drop_marble(
                move['position'],
                move['color']
            )
        
        # Update board state after move
        self.board.update()

    # Check if current board state satisfies challenge conditions
    def _check_solution(self, challenge_config: Dict) -> bool:
        # Get current outputs from the board
        current_outputs = self.board.outputs
        
        # Compare with expected outputs from challenge
        expected_outputs = challenge_config.get('expected_outputs', {})
        
        return current_outputs == expected_outputs

    # Calculate and return success rate
    def get_success_rate(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.success_count / self.total_attempts

    # Reset success statistics
    def reset_stats(self) -> None:
        self.success_count = 0
        self.total_attempts = 0
