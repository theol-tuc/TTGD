import os
import networkx as nx
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import matplotlib.pyplot as plt

# === STEP 1: Load .gv File and Convert to NetworkX Graph ===
def load_puzzle_graph(file_path):
    # Load a puzzle from a Graphviz .gv file into a NetworkX graph
    return nx.nx_pydot.read_dot(file_path)

# === STEP 2: Convert Graph to PyTorch Geometric Format ===
def graph_to_data(graph):
    # Create a mapping from node labels to integer indices
    node_mapping = {node: i for i, node in enumerate(graph.nodes)}
    features = []

    # Convert each node into a binary feature vector based on type (ball, gear, etc.)
    for node in graph.nodes:
        label = graph.nodes[node].get('label', '').lower()
        feat = [
            'ball' in label,
            'bit' in label,
            'gear' in label,
            'interceptor' in label,
            'crossover' in label,
            'ramp' in label,
            'toggle' in label,
            'output' in label
        ]
        features.append(torch.tensor(feat, dtype=torch.float))

    # Build edge list for the graph
    edge_index = []
    for src, dst in graph.edges:
        edge_index.append([node_mapping[src], node_mapping[dst]])

    # Prepare PyTorch Geometric Data object
    x = torch.stack(features)
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    return Data(x=x, edge_index=edge_index)

# === STEP 3: Define the Symbolic Reasoning GNN ===
class SymbolicGNN(torch.nn.Module):
    def __init__(self, in_features=8, hidden=32, out_features=8):
        super().__init__()
        # Two GCN layers to process the logic graph
        self.conv1 = GCNConv(in_features, hidden)
        self.conv2 = GCNConv(hidden, out_features)

    def forward(self, x, edge_index):
        # Apply GCN with ReLU, then second layer
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

# === STEP 4: GPT-2 Based Transformer Planner ===
class TransformerPlanner:
    def __init__(self):
        # Load pretrained GPT-2 model and tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")

    def generate_plan(self, symbolic_output):
        # Turn symbolic output into a string prompt for GPT-2
        input_tokens = " ".join([f"{i}:{','.join(map(str, f.tolist()))}" for i, f in enumerate(symbolic_output)])
        inputs = self.tokenizer.encode(input_tokens, return_tensors="pt")
        # Let GPT-2 generate a plan using symbolic context
        outputs = self.model.generate(inputs, max_length=100, num_return_sequences=1)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# === STEP 5: Hybrid Agent Combining GNN + Transformer ===
class HybridPuzzleAgent:
    def __init__(self):
        self.gnn = SymbolicGNN()  # symbolic processor
        self.planner = TransformerPlanner()  # planning engine

    def solve(self, graph):
        # Convert graph to data, apply GNN, then plan with Transformer
        data = graph_to_data(graph)
        symbolic_output = self.gnn(data.x, data.edge_index)
        return self.planner.generate_plan(symbolic_output)

# === STEP 6: Main Runner ===
def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the puzzle file
    puzzle_path = os.path.join(script_dir, "puzzle08.gv")

    if not os.path.exists("C:\Users\rohit\OneDrive\Desktop\TuringTumble\Challenges\puzzle08n.gv"):
        print(f"Puzzle file not found: {"C:\Users\rohit\OneDrive\Desktop\TuringTumble\Challenges\puzzle08n.gv"}")
        return

    graph = load_puzzle_graph("C:\Users\rohit\OneDrive\Desktop\TuringTumble\Challenges\puzzle08n.gv")
    agent = HybridPuzzleAgent()
    plan = agent.solve(graph)

    # Print the AI-generated plan
    print("Generated Plan:")
    print(plan)

    # Visualize the logic graph for understanding
    nx.draw(graph, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title("Turing Tumble Puzzle Graph")
    plt.savefig('puzzle_graph.png')

if __name__ == "__main__":
    main()