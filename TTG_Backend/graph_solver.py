import os
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import Data
import numpy as np
from .game_logic import GameBoard, ComponentType, BLUE
from .board_encoder import BoardEncoder
import sys
sys.path.append('../LLaVA')
from llava.model import LlavaLlamaForCausalLM
from llava.conversation import conv_templates
from llava.utils import disable_torch_init
from llava.mm_utils import process_images, tokenizer_image_token
from PIL import Image
import networkx as nx
from typing import List, Dict, Tuple
from enum import Enum
from challenges import CHALLENGES

# Set device to CUDA if available, otherwise use CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

class ComponentType(Enum):
    EMPTY = 0
    RAMP = 1
    GEAR = 2
    CROSSOVER = 3
    AND_GATE = 4
    OR_GATE = 5
    BIT = 6

class GraphNeuralNetwork(nn.Module):
    def __init__(self, num_node_features: int, num_classes: int):
        super(GraphNeuralNetwork, self).__init__()
        self.conv1 = GCNConv(num_node_features, 64)
        self.conv2 = GCNConv(64, 32)
        self.classifier = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, num_classes)
        )
    
    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        x = torch.relu(x)
        x = self.classifier(x)
        return x

class GraphSolver:
    def __init__(self, llava_model=None):
        print("Initializing Graph Solver...")
        # Initialize LLaVA for visual understanding
        if llava_model and os.path.exists(llava_model):
            print(f"Loading LLaVA model from: {llava_model}")
            disable_torch_init()
            self.llava_model = LlavaLlamaForCausalLM.from_pretrained(
                llava_model,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.tokenizer = self.llava_model.get_tokenizer()
            self.image_processor = self.llava_model.get_image_processor()
        else:
            raise ValueError("LLaVA model path not provided or invalid")
        
        # Initialize Graph Neural Network
        self.gnn = GraphNeuralNetwork(
            num_node_features=10,  # Features per node (component type, position, etc.)
            num_classes=len(ComponentType)  # Number of possible component types
        ).to(device)
        
        print(f"Models loaded on {device}")

    def board_to_graph(self, board) -> Data:
        """Convert board state to graph representation with enhanced features"""
        num_nodes = len(board.components)
        node_features = []
        edge_index = []
        
        # Create node features with enhanced information
        for i, component in enumerate(board.components):
            features = [
                component.position[0] / board.width,  # Normalized x position
                component.position[1] / board.height,  # Normalized y position
                component.type.value / len(ComponentType),  # Normalized type
                component.state if hasattr(component, 'state') else 0,  # Component state
                component.rotation if hasattr(component, 'rotation') else 0,  # Rotation
                component.is_active if hasattr(component, 'is_active') else 0,  # Active state
                component.connections.count(True) / 8 if hasattr(component, 'connections') else 0,  # Connection density
                component.value if hasattr(component, 'value') else 0,  # Value (for bits)
                component.is_output if hasattr(component, 'is_output') else 0,  # Output status
                component.is_input if hasattr(component, 'is_input') else 0,  # Input status
            ]
            node_features.append(features)
        
        # Create edges based on component connections and board layout
        for i, component in enumerate(board.components):
            # Add edges for physical connections
            if hasattr(component, 'connections'):
                for j, connected in enumerate(component.connections):
                    if connected:
                        edge_index.append([i, j])
                        edge_index.append([j, i])  # Bidirectional
            
            # Add edges for logical connections (for gates)
            if component.type in [ComponentType.AND_GATE, ComponentType.OR_GATE]:
                for j, other in enumerate(board.components):
                    if other.is_input and self._is_connected(component, other):
                        edge_index.append([i, j])
                        edge_index.append([j, i])
        
        # Convert to PyTorch tensors
        x = torch.tensor(node_features, dtype=torch.float)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        
        return Data(x=x, edge_index=edge_index)
    
    def _is_connected(self, comp1, comp2) -> bool:
        """Check if two components are logically connected"""
        if not hasattr(comp1, 'position') or not hasattr(comp2, 'position'):
            return False
        
        # Check physical proximity
        dist = np.sqrt((comp1.position[0] - comp2.position[0])**2 + 
                      (comp1.position[1] - comp2.position[1])**2)
        return dist <= 2  # Components within 2 units are considered connected
    
    def analyze_board(self, board_image_path: str = None) -> str:
        """Analyze the board using LLaVA if available"""
        if self.llava_model and board_image_path:
            # Use LLaVA for visual analysis
            return self.llava_model.analyze_image(board_image_path)
        return "Board analysis not available"
    
    def generate_solution(self, board, board_image_path: str = None) -> List[Dict]:
        """Generate solution using both GNN and LLaVA"""
        # Convert board to graph
        graph_data = self.board_to_graph(board)
        
        # Get GNN predictions
        with torch.no_grad():
            predictions = self.gnn(
                graph_data.x,
                graph_data.edge_index,
                torch.zeros(len(graph_data.x), dtype=torch.long)
            )
        
        # Get LLaVA analysis if available
        llava_analysis = self.analyze_board(board_image_path)
        
        # Combine predictions and analysis
        solution = self._combine_predictions(predictions, llava_analysis, board)
        return solution
    
    def _combine_predictions(self, predictions, llava_analysis: str, board) -> List[Dict]:
        """Combine GNN predictions with LLaVA analysis"""
        solution = []
        
        # Process GNN predictions
        pred_indices = torch.topk(predictions, k=3)[1]
        for idx in pred_indices:
            component_type = ComponentType(idx.item())
            if component_type != ComponentType.EMPTY:
                solution.append({
                    'type': component_type.name,
                    'confidence': predictions[0][idx].item(),
                    'source': 'GNN'
                })
        
        # Add LLaVA insights if available
        if llava_analysis != "Board analysis not available":
            solution.append({
                'type': 'ANALYSIS',
                'content': llava_analysis,
                'source': 'LLaVA'
            })
        
        return solution
    
    def parse_solution(self, solution: List[Dict]) -> str:
        """Convert solution to human-readable format"""
        steps = []
        for item in solution:
            if item['type'] == 'ANALYSIS':
                steps.append(f"Analysis: {item['content']}")
            else:
                steps.append(
                    f"Place {item['type']} (confidence: {item['confidence']:.2f})"
                )
        return "\n".join(steps)

def solve_challenge(board, board_image_path: str = None, llava_model_path: str = None):
    """Main function to solve a challenge"""
    try:
        print("Starting challenge solver...")
        
        # Initialize the solver
        solver = GraphSolver(llava_model_path)
        
        # Generate and parse solution
        solution = solver.generate_solution(board, board_image_path)
        print("Generated Solution:")
        print(solver.parse_solution(solution))
        
        return {
            "solution": solver.parse_solution(solution)
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

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