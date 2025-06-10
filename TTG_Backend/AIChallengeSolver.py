# AI-based puzzle solver using GPT-4 for enhanced puzzle solving
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Optional
import numpy as np
import json
from datetime import datetime
from game_logic import GameBoard, ComponentType, BLUE, RED
import openai
import os
from dotenv import load_dotenv
from TuringTumble import TransformerPlanner
from .graph_solver import GraphSolver

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = "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"

# Initialize components
COMPONENTS = {
    ComponentType.RAMP_LEFT: {
        'name': 'Ramp Left',
        'description': 'Moves marbles to the left',
        'state': 'active'
    },
    ComponentType.RAMP_RIGHT: {
        'name': 'Ramp Right',
        'description': 'Moves marbles to the right',
        'state': 'active'
    },
    ComponentType.CROSSOVER: {
        'name': 'Crossover',
        'description': 'Allows marbles to cross paths',
        'state': 'active'
    },
    ComponentType.GEAR: {
        'name': 'Gear',
        'description': 'Binary gear that can be toggled',
        'state': 'active'
    },
    ComponentType.INTERCEPTOR: {
        'name': 'Interceptor',
        'description': 'Stops marbles',
        'state': 'active'
    }
}

# Main solver class using GPT-4 for enhanced puzzle solving
class AIChallengeSolver:
    def __init__(self):
        """Initialize the AI solver with GPT-4."""
        self.board = GameBoard()
        self.solution_steps = []
        self.total_attempts = 0
        self.success_count = 0
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=openai.api_key)
        
        # Initialize graph solver
        self.graph_solver = GraphSolver()
        
        # Initialize temperature for GPT-4
        self.temperature = 0.7
        
        # Initialize GPT-4
        self.model = "gpt-4"
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")
        
        # Initialize game board for puzzle solving
        self.board = GameBoard()
        
        # Track solution steps for analysis
        self.solution_steps = []
        
        # Track success rate metrics
        self.success_count = 0
        self.total_attempts = 0
        
        # Initialize enhanced features
        self.context_window = []
        self.max_context_length = 10
        self.max_tokens = 150

    def prepare_input(self, board_state: np.ndarray) -> str:
        # Convert board state to a descriptive prompt
        board_description = self._board_state_to_description(board_state)
        return board_description

    def _board_state_to_description(self, board_state: np.ndarray) -> str:
        # Convert numpy array to human-readable description
        description = "Current board state:\n"
        for y in range(board_state.shape[0]):
            for x in range(board_state.shape[1]):
                component = board_state[y, x]
                if component != 0:
                    description += f"Position ({x}, {y}): {ComponentType(component).name}\n"
        return description

    def generate_move(self, board_state: np.ndarray) -> Dict:
        # Prepare input description
        board_description = self.prepare_input(board_state)
        
        # Create system message
        system_message = {
            "role": "system",
            "content": "You are an expert Turing Tumble puzzle solver. Analyze the board state and suggest the next optimal move."
        }
        
        # Create user message with board state
        user_message = {
            "role": "user",
            "content": board_description
        }
        
        # Add context from previous moves
        messages = [system_message]
        messages.extend(self.context_window)
        messages.append(user_message)
        
        try:
            # Generate response using GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Process the response
            move = self._process_model_output(response.choices[0].message.content)
            
            # Update context window
            self._update_context_window(user_message, response.choices[0].message)
            
            return move
            
        except Exception as e:
            print(f"Error generating move: {str(e)}")
            return self._generate_fallback_move(board_state)

    def _process_model_output(self, response: str) -> Dict:
        # Parse the GPT-4 response to extract move information
        try:
            # Extract move information from the response
            # This is a simplified version - you might want to add more robust parsing
            if "drop" in response.lower():
                color = BLUE if "blue" in response.lower() else RED
                position = self._extract_position(response)
                return {
                    'type': 'drop_marble',
                    'position': position,
                    'color': color
                }
            else:
                return self._generate_fallback_move(self.board.get_board_state())
        except Exception as e:
            print(f"Error processing model output: {str(e)}")
            return self._generate_fallback_move(self.board.get_board_state())

    def _extract_position(self, response: str) -> int:
        # Extract position from the response
        # This is a simplified version - you might want to add more robust parsing
        try:
            # Look for position information in the response
            if "position" in response.lower():
                # Extract the position number
                position_str = response.split("position")[1].split()[0]
                return int(position_str)
            return 7  # Default to middle position
        except:
            return 7  # Default to middle position

    def _generate_fallback_move(self, board_state: np.ndarray) -> Dict:
        # Generate a fallback move when the model fails
        return {
            'type': 'drop_marble',
            'position': 7,  # Middle position
            'color': BLUE
        }

    def _update_context_window(self, user_message: Dict, assistant_message: Dict):
        # Update the context window with the latest interaction
        self.context_window.append(user_message)
        self.context_window.append(assistant_message)
        
        # Keep only the last N interactions
        if len(self.context_window) > self.max_context_length * 2:
            self.context_window = self.context_window[-self.max_context_length * 2:]

    def solve_challenge(self, challenge_config: Dict) -> List[Dict]:
        """Solve a challenge using both GPT-4 and graph-based approaches."""
        self.total_attempts += 1
        
        # Reset the board
        self.board.clear()
        
        # Add components from challenge config
        for comp in challenge_config.get('components', []):
            self.board.add_component(ComponentType[comp['type']], comp['x'], comp['y'])
        
        # Add marbles
        for _ in range(challenge_config.get('red_marbles', 0)):
            self.board.add_marble(RED)
        for _ in range(challenge_config.get('blue_marbles', 0)):
            self.board.add_marble(BLUE)
        
        # Try graph-based solution first
        try:
            graph_solution = self.graph_solver.solve(self.board)
            if graph_solution:
                self.solution_steps.extend(graph_solution)
                self.success_count += 1
                return self.solution_steps
        except Exception as e:
            print(f"Graph solving failed: {str(e)}")
        
        # Fall back to GPT-4 if graph solving fails
        try:
            gpt_solution = self._solve_with_gpt(challenge_config)
            if gpt_solution:
                self.solution_steps.extend(gpt_solution)
                self.success_count += 1
                return self.solution_steps
        except Exception as e:
            print(f"GPT solving failed: {str(e)}")
        
        return []

    def _solve_with_gpt(self, challenge_config: Dict) -> List[Dict]:
        """Solve the challenge using GPT-4."""
        # Prepare the prompt for GPT-4
        prompt = self._create_prompt(challenge_config)
        
        # Get response from GPT-4
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Turing Tumble puzzle solver."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        # Parse and validate the solution
        solution = self._parse_gpt_response(response.choices[0].message.content)
        if solution:
            return solution
        return []

    def _create_prompt(self, challenge_config: Dict) -> str:
        """Create a prompt for GPT-4 based on the challenge configuration."""
        components = "\n".join([f"- {comp['type']} at ({comp['x']}, {comp['y']})" 
                              for comp in challenge_config.get('components', [])])
        
        return f"""Solve this Turing Tumble puzzle:
Components:
{components}

Red marbles: {challenge_config.get('red_marbles', 0)}
Blue marbles: {challenge_config.get('blue_marbles', 0)}

Expected outputs:
{challenge_config.get('expected_outputs', {})}

Provide a step-by-step solution."""

    def _parse_gpt_response(self, response: str) -> List[Dict]:
        """Parse the GPT-4 response into a list of moves."""
        moves = []
        try:
            # Parse the response and convert to moves
            # This is a simplified version - you might need to enhance it
            lines = response.split('\n')
            for line in lines:
                if 'move' in line.lower() or 'drop' in line.lower():
                    moves.append({'type': 'move', 'description': line.strip()})
            return moves
        except Exception as e:
            print(f"Error parsing GPT response: {str(e)}")
            return []

    def get_success_rate(self) -> float:
        """Calculate and return the success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.success_count / self.total_attempts

    def _send_to_mcp(self, data: Dict) -> None:
        """
        Send data to the Model Context Protocol (MCP).
        This method handles the communication with the MCP.
        """
        try:
            # Convert data to JSON format
            mcp_data = {
                'solver': 'AIChallengeSolver',
                'timestamp': self._get_timestamp(),
                'board_state': self.board.send_to_mcp(),
                'solution_steps': self.solution_steps,
                'metrics': {
                    'success_rate': self.get_success_rate(),
                    'total_attempts': self.total_attempts,
                    'success_count': self.success_count
                },
                'additional_data': data
            }
            
            # Here you would typically send the data to the MCP
            # For now, we'll just print it
            print("MCP Data:", json.dumps(mcp_data, indent=2))
            
        except Exception as e:
            print(f"Error sending data to MCP: {str(e)}")

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def solve_challenge_with_mcp(self, challenge_config: Dict) -> List[Dict]:
        """
        Solve a challenge and report results to the MCP.
        """
        # Solve the challenge
        solution = self.solve_challenge(challenge_config)
        
        # Send results to MCP
        self._send_to_mcp({
            'challenge_config': challenge_config,
            'solution': solution,
            'success': self._check_solution(challenge_config)
        })
        
        return solution

    # Calculate and return success rate
    def get_success_rate(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.success_count / self.total_attempts

    # Reset success statistics
    def reset_stats(self) -> None:
        self.success_count = 0
        self.total_attempts = 0
