# Training script for VILLA-based graph puzzle solver
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import os
import json
import networkx as nx
from typing import Dict, List, Tuple
from tqdm import tqdm
import numpy as np
from .villa_solver import VILLASolver, GraphNeuralNetwork
from .game_logic import ComponentType

class GraphPuzzleDataset(Dataset):
    def __init__(self, data_dir: str, split: str = 'train'):
        """
        Dataset for graph-based puzzles
        Args:
            data_dir: Directory containing puzzle graphs and annotations
            split: 'train', 'val', or 'test'
        """
        self.data_dir = data_dir
        self.split = split
        
        # Load puzzle metadata
        metadata_path = os.path.join(data_dir, f'{split}_metadata.json')
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Load graph paths and annotations
        self.graph_paths = []
        self.annotations = []
        
        for puzzle_id, puzzle_data in self.metadata.items():
            graph_path = os.path.join(data_dir, f'{puzzle_id}.dot')
            if os.path.exists(graph_path):
                self.graph_paths.append(graph_path)
                self.annotations.append(puzzle_data)
    
    def __len__(self) -> int:
        return len(self.graph_paths)
    
    def __getitem__(self, idx: int) -> Tuple[nx.Graph, Dict]:
        # Load graph
        graph = nx.nx_pydot.read_dot(self.graph_paths[idx])
        
        # Get annotation
        annotation = self.annotations[idx]
        
        return graph, annotation

def train_villa(
    data_dir: str,
    output_dir: str,
    num_epochs: int = 100,
    batch_size: int = 32,
    learning_rate: float = 1e-4,
    weight_decay: float = 1e-5
):
    """
    Train the VILLA-based graph puzzle solver
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize solver
    solver = VILLASolver()
    
    # Create datasets
    train_dataset = GraphPuzzleDataset(data_dir, 'train')
    val_dataset = GraphPuzzleDataset(data_dir, 'val')
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4
    )
    
    # Initialize optimizer
    optimizer = optim.AdamW(
        solver.gnn.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay
    )
    
    # Initialize loss function
    criterion = nn.CrossEntropyLoss()
    
    # Training loop
    best_val_loss = float('inf')
    for epoch in range(num_epochs):
        # Training phase
        solver.gnn.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for graphs, annotations in tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}'):
            # Convert graphs to PyTorch Geometric format
            data_list = [solver.graph_to_data(g) for g in graphs]
            
            # Prepare targets
            targets = []
            for ann in annotations:
                target = torch.zeros(len(ComponentType))
                for comp in ann['components']:
                    target[ComponentType[comp['type']].value] = 1
                targets.append(target)
            targets = torch.stack(targets).to(solver.device)
            
            # Forward pass
            optimizer.zero_grad()
            for data in data_list:
                data = data.to(solver.device)
                outputs = solver.gnn(data.x, data.edge_index)
                loss = criterion(outputs, targets)
                loss.backward()
                train_loss += loss.item()
                
                # Calculate accuracy
                pred = torch.argmax(outputs, dim=1)
                true = torch.argmax(targets, dim=1)
                train_correct += (pred == true).sum().item()
                train_total += len(true)
            
            optimizer.step()
        
        # Calculate training metrics
        avg_train_loss = train_loss / len(train_loader)
        train_accuracy = train_correct / train_total
        
        # Validation phase
        solver.gnn.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for graphs, annotations in val_loader:
                # Convert graphs to PyTorch Geometric format
                data_list = [solver.graph_to_data(g) for g in graphs]
                
                # Prepare targets
                targets = []
                for ann in annotations:
                    target = torch.zeros(len(ComponentType))
                    for comp in ann['components']:
                        target[ComponentType[comp['type']].value] = 1
                    targets.append(target)
                targets = torch.stack(targets).to(solver.device)
                
                # Forward pass
                for data in data_list:
                    data = data.to(solver.device)
                    outputs = solver.gnn(data.x, data.edge_index)
                    loss = criterion(outputs, targets)
                    val_loss += loss.item()
                    
                    # Calculate accuracy
                    pred = torch.argmax(outputs, dim=1)
                    true = torch.argmax(targets, dim=1)
                    val_correct += (pred == true).sum().item()
                    val_total += len(true)
        
        # Calculate validation metrics
        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = val_correct / val_total
        
        # Print metrics
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'Train Loss: {avg_train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}')
        print(f'Val Loss: {avg_val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}')
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': solver.gnn.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': avg_train_loss,
                'val_loss': avg_val_loss,
                'train_accuracy': train_accuracy,
                'val_accuracy': val_accuracy
            }, os.path.join(output_dir, 'best_model.pth'))
            
            print(f'New best model saved with validation loss: {best_val_loss:.4f}')

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train VILLA-based graph puzzle solver')
    parser.add_argument('--data_dir', type=str, required=True, help='Directory containing puzzle data')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save model checkpoints')
    parser.add_argument('--num_epochs', type=int, default=100, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--learning_rate', type=float, default=1e-4, help='Learning rate')
    parser.add_argument('--weight_decay', type=float, default=1e-5, help='Weight decay')
    
    args = parser.parse_args()
    
    train_villa(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay
    ) 