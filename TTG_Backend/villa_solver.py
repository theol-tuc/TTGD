# VILLA-based graph puzzle solver for Turing Tumble
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv
from .game_logic import ComponentType
import networkx as nx
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

# Load environment variables
load_dotenv()

class VILLASolver:
    def __init__(self, model_path: Optional[str] = None):
        # Initialize VILLA model and tokenizer
        self.model_name = "microsoft/villa-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        
        # Move model to GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Initialize graph neural network
        self.gnn = GraphNeuralNetwork(
            num_node_features=10,  # Features per node
            num_classes=len(ComponentType)
        ).to(self.device)
        
        # Load pre-trained weights if provided
        if model_path and os.path.exists(model_path):
            self._load_weights(model_path)

    def _load_weights(self, model_path: str):
        """Load pre-trained weights for GNN"""
        try:
            weights = torch.load(model_path, map_location=self.device)
            self.gnn.load_state_dict(weights['gnn'])
            print("Successfully loaded pre-trained weights")
        except Exception as e:
            print(f"Error loading weights: {str(e)}")

    def graph_to_data(self, graph: nx.Graph) -> Data:
        """
        Convert NetworkX graph to PyTorch Geometric Data object
        """
        # Create node features
        node_features = []
        for node in graph.nodes():
            features = [
                graph.nodes[node].get('x', 0) / 15,  # Normalized x position
                graph.nodes[node].get('y', 0) / 17,  # Normalized y position
                graph.nodes[node].get('type', 0) / len(ComponentType),  # Normalized type
                graph.nodes[node].get('state', 0),  # Component state
                graph.nodes[node].get('rotation', 0),  # Rotation
                graph.nodes[node].get('is_active', 0),  # Active state
                graph.nodes[node].get('connections', 0) / 8,  # Connection density
                graph.nodes[node].get('value', 0),  # Value
                graph.nodes[node].get('is_output', 0),  # Output status
                graph.nodes[node].get('is_input', 0),  # Input status
            ]
            node_features.append(features)
        
        # Create edge index
        edge_index = []
        for edge in graph.edges():
            edge_index.append([edge[0], edge[1]])
            edge_index.append([edge[1], edge[0]])  # Bidirectional
        
        # Convert to tensors
        x = torch.tensor(node_features, dtype=torch.float)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        
        return Data(x=x, edge_index=edge_index)

    def analyze_graph(self, graph_path: str) -> Dict:
        """
        Analyze a puzzle graph using VILLA model
        """
        try:
            # Load graph from file
            graph = nx.nx_pydot.read_dot(graph_path)
            
            # Convert graph to PyTorch Geometric format
            data = self.graph_to_data(graph)
            data = data.to(self.device)
            
            # Get GNN predictions
            with torch.no_grad():
                predictions = self.gnn(data.x, data.edge_index)
            
            # Process predictions
            component_info = self._process_predictions(predictions, graph)
            
            return {
                'status': 'success',
                'components': component_info,
                'graph': graph
            }
            
        except Exception as e:
            print(f"Error analyzing graph: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _process_predictions(self, predictions: torch.Tensor, graph: nx.Graph) -> List[Dict]:
        """
        Process GNN predictions to extract component information
        """
        components = []
        
        # Get predictions for each node
        pred_indices = torch.argmax(predictions, dim=1)
        confidences = torch.softmax(predictions, dim=1).max(dim=1)[0]
        
        for i, (pred_idx, conf) in enumerate(zip(pred_indices, confidences)):
            if conf > 0.5:  # Confidence threshold
                node = list(graph.nodes())[i]
                component = {
                    'type': ComponentType(pred_idx.item()).name,
                    'confidence': conf.item(),
                    'position': (
                        graph.nodes[node].get('x', 0),
                        graph.nodes[node].get('y', 0)
                    )
                }
                components.append(component)
        
        return components

    def get_graph_insights(self, graph_path: str) -> str:
        """
        Get human-readable insights about the puzzle graph
        """
        analysis = self.analyze_graph(graph_path)
        
        if analysis['status'] == 'success':
            insights = []
            for comp in analysis['components']:
                insight = f"Found {comp['type']} at position {comp['position']} with confidence {comp['confidence']:.2f}"
                insights.append(insight)
            return "\n".join(insights)
        else:
            return f"Error analyzing graph: {analysis['message']}"

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
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        x = torch.relu(x)
        x = self.classifier(x)
        return x 