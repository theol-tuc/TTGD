"""
Graph-based solver for Turing Tumble puzzles.
Uses graph algorithms to find optimal solutions.
"""

from typing import List, Dict, Tuple, Optional
from game_logic import GameBoard, ComponentType, BLUE, RED
import networkx as nx
import numpy as np
import torch

class GraphSolver:
    def __init__(self):
        """Initialize the graph solver."""
        self.graph = nx.DiGraph()
        self.solution_path = []
        
    def solve(self, board: GameBoard) -> List[Dict]:
        """
        Solve the puzzle using graph-based approach.
        Returns a list of moves to solve the puzzle.
        """
        # Build the graph representation of the board
        self._build_graph(board)
        
        # Find the optimal path
        path = self._find_optimal_path(board)
        
        # Convert path to moves
        moves = self._path_to_moves(path, board)
        
        return moves
    
    def _build_graph(self, board: GameBoard) -> None:
        """Build a graph representation of the board."""
        self.graph.clear()
        
        # Add nodes for each component
        for comp in board.components:
            self.graph.add_node(comp.position, type=comp.type)
        
        # Add edges based on component connections
        for comp in board.components:
            x, y = comp.position
            # Add edges based on component type
            if comp.type == ComponentType.RAMP_LEFT:
                if x > 0:
                    self.graph.add_edge(comp.position, (x-1, y+1))
            elif comp.type == ComponentType.RAMP_RIGHT:
                if x < board.width - 1:
                    self.graph.add_edge(comp.position, (x+1, y+1))
            elif comp.type == ComponentType.CROSSOVER:
                if x > 0 and x < board.width - 1:
                    self.graph.add_edge(comp.position, (x-1, y+1))
                    self.graph.add_edge(comp.position, (x+1, y+1))
    
    def _find_optimal_path(self, board: GameBoard) -> List[Tuple[int, int]]:
        """Find the optimal path through the graph."""
        # Find all possible start positions (top row)
        start_positions = [(x, 0) for x in range(board.width)]
        
        # Find all possible end positions (bottom row)
        end_positions = [(x, board.height-1) for x in range(board.width)]
        
        # Try to find a path from any start to any end
        for start in start_positions:
            for end in end_positions:
                try:
                    path = nx.shortest_path(self.graph, start, end)
                    return path
                except nx.NetworkXNoPath:
                    continue
        
        return []
    
    def _path_to_moves(self, path: List[Tuple[int, int]], board: GameBoard) -> List[Dict]:
        """Convert a path to a list of moves."""
        moves = []
        if not path:
            return moves
        
        # Add initial marble drop
        start_x = path[0][0]
        moves.append({
            'type': 'drop_marble',
            'position': start_x,
            'color': BLUE
        })
        
        # Add component interactions
        for i in range(len(path)-1):
            current = path[i]
            next_pos = path[i+1]
            
            # Find the component at the current position
            comp = next((c for c in board.components if c.position == current), None)
            if comp:
                moves.append({
                    'type': 'interact',
                    'component': comp.type.name,
                    'position': current
                })
        
        return moves

# Main function to solve a challenge using the GraphSolver
def solve_challenge(board, board_image_path: str = None, llava_model_path: str = None):
    try:
        print("Starting challenge solver...")
        
        # Initialize the solver
        solver = GraphSolver()
        
        # Generate and parse solution
        solution = solver.solve(board)
        print("Generated Solution:")
        print(solution)
        
        return {
            "solution": solution
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Example usage and testing
if __name__ == '__main__':
    print("Script started")
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("Number of GPUs:", torch.cuda.device_count())
        print("GPU Name:", torch.cuda.get_device_name(0))
    else:
        print("Running on CPU mode")
    
    # Example usage
    from challenges import create_challenge_1_board
    
    # Create a challenge board
    board = create_challenge_1_board()
    
    # Update these paths to your actual model and image paths
    llava_model_path = "../LLaVA/llava-v1.5-13b"
    board_image_path = "path/to/your/board/image.jpg"  # Optional
    
    result = solve_challenge(board, board_image_path, llava_model_path)
    if result:
        print("\nChallenge solved successfully!")
    else:
        print("\nFailed to solve the challenge.") 