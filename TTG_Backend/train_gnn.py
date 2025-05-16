import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.loader import DataLoader
from graph_solver import GraphNeuralNetwork, GraphSolver
from challenges import CHALLENGES
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

def create_training_dataset():
    """Create a dataset from the challenges"""
    dataset = []
    for challenge_id, challenge in CHALLENGES.items():
        board = challenge["board"]
        solver = GraphSolver(None)  # Initialize without LLaVA for training
        graph_data = solver.board_to_graph(board)
        # Add target labels (optimal component placements)
        target = torch.zeros(len(ComponentType))
        for component in board.components:
            if component.type != ComponentType.EMPTY:
                target[component.type.value] = 1
        graph_data.y = target
        dataset.append(graph_data)
    return dataset

def train_gnn(model, train_loader, optimizer, criterion, device, epochs=100):
    """Train the GNN model"""
    model.train()
    losses = []
    
    for epoch in range(epochs):
        epoch_loss = 0
        for batch in tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}'):
            batch = batch.to(device)
            optimizer.zero_grad()
            
            # Forward pass
            out = model(batch.x, batch.edge_index, batch.batch)
            loss = criterion(out, batch.y)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        avg_loss = epoch_loss / len(train_loader)
        losses.append(avg_loss)
        print(f'Epoch {epoch+1}, Loss: {avg_loss:.4f}')
    
    return losses

def plot_training_loss(losses, save_path='training_loss.png'):
    """Plot the training loss curve"""
    plt.figure(figsize=(10, 6))
    plt.plot(losses)
    plt.title('Training Loss Over Time')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

def save_model(model, path='gnn_model.pth'):
    """Save the trained model"""
    torch.save(model.state_dict(), path)

def load_model(model, path='gnn_model.pth'):
    """Load a trained model"""
    model.load_state_dict(torch.load(path))
    return model

def main():
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create dataset
    print("Creating training dataset...")
    dataset = create_training_dataset()
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Initialize model
    model = GraphNeuralNetwork(
        num_node_features=10,
        num_classes=len(ComponentType)
    ).to(device)
    
    # Training setup
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCEWithLogitsLoss()
    
    # Train model
    print("Starting training...")
    losses = train_gnn(model, train_loader, optimizer, criterion, device)
    
    # Plot and save results
    plot_training_loss(losses)
    save_model(model)
    
    print("Training completed!")
    print(f"Final loss: {losses[-1]:.4f}")

if __name__ == '__main__':
    main() 