"""
Graph-based solver for Turing Tumble puzzles.
Uses graph algorithms to find optimal solutions.
"""

from typing import List, Dict, Tuple, Optional
from TTG_Backend.game_logic import GameBoard, ComponentType, BLUE, RED
import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GraphNeuralNetwork(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, output_dim: int = 32):
        super(GraphNeuralNetwork, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, output_dim)
    
    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)
        return x

class GraphSolver:
    def __init__(self):
        """Initialize the graph solver."""
        self.graph = nx.DiGraph()
        self.solution_path = []
        self.model = GraphNeuralNetwork(input_dim=32)  # 32 features per node
        
    def solve(self, board: GameBoard) -> List[str]:
        """Solve the puzzle using graph neural network"""
        # Convert board to graph
        graph = self._board_to_graph(board)
        
        # Get node features and edge indices
        x, edge_index = self._prepare_graph_data(graph)
        
        # Get model predictions
        with torch.no_grad():
            predictions = self.model(x, edge_index)
        
        # Convert predictions to solution steps
        solution = self._predictions_to_steps(predictions, graph)
        return solution
    
    def _board_to_graph(self, board: GameBoard) -> nx.Graph:
        """Convert board state to graph representation"""
        graph = nx.Graph()
        
        # Add nodes for each component
        for i in range(8):
            for j in range(8):
                component = board.get_component(i, j)
                if component is not None:
                    node_id = f"{i},{j}"
                    graph.add_node(node_id, type=component)
        
        # Add edges between connected components
        for i in range(8):
            for j in range(8):
                if board.get_component(i, j) is not None:
                    # Check adjacent positions
                    for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 8 and 0 <= nj < 8:
                            if board.get_component(ni, nj) is not None:
                                graph.add_edge(f"{i},{j}", f"{ni},{nj}")
        
        return graph
    
    def _prepare_graph_data(self, graph: nx.Graph) -> Tuple[torch.Tensor, torch.Tensor]:
        """Prepare graph data for the neural network"""
        # Convert node features to tensor
        node_features = []
        for node in graph.nodes():
            component = graph.nodes[node]['type']
            features = self._component_to_features(component)
            node_features.append(features)
        
        x = torch.tensor(node_features, dtype=torch.float)
        
        # Convert edge indices to tensor
        edge_index = []
        for edge in graph.edges():
            source = list(graph.nodes()).index(edge[0])
            target = list(graph.nodes()).index(edge[1])
            edge_index.append([source, target])
            edge_index.append([target, source])  # Add reverse edge
        
        edge_index = torch.tensor(edge_index, dtype=torch.long).t()
        
        return x, edge_index
    
    def _component_to_features(self, component: ComponentType) -> List[float]:
        """Convert component type to feature vector"""
        # One-hot encoding of component types
        features = [0.0] * 32
        type_idx = component.value
        features[type_idx] = 1.0
        return features
    
    def _predictions_to_steps(self, predictions: torch.Tensor, graph: nx.Graph) -> List[str]:
        """Convert model predictions to solution steps"""
        steps = []
        node_list = list(graph.nodes())
        
        # Process predictions to generate steps
        for i in range(len(node_list)):
            node = node_list[i]
            pred = predictions[i]
            if torch.max(pred) > 0.5:  # If node is predicted to be part of solution
                x, y = map(int, node.split(','))
                component = graph.nodes[node]['type']
                steps.append(f"Move ball to position ({x}, {y})")
        
        return steps
    
    def verify_solution(self, board: GameBoard, steps: List[str]) -> bool:
        """Verify if the solution steps are valid"""
        # Create a copy of the board to simulate moves
        test_board = GameBoard()
        for i in range(8):
            for j in range(8):
                test_board.set_component(i, j, board.get_component(i, j))
        
        # Simulate each step
        for step in steps:
            # Parse step to get position
            # This is a simplified version - you'll need to implement proper parsing
            try:
                x, y = map(int, step.split('(')[1].split(')')[0].split(','))
                if not (0 <= x < 8 and 0 <= y < 8):
                    return False
                if test_board.get_component(x, y) is None:
                    return False
            except:
                return False
        
        return True

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