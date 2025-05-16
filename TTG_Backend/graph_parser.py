import os
import re
from typing import Dict, List, Tuple
from TTG_Backend.game_logic import GameBoard, ComponentType
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import json
# from TTG_Backend.challenges import CHALLENGES  # Removed to fix circular import

class GraphVizParser:
    def __init__(self, challenges_dir: str = "../Challenges"):
        self.challenges_dir = challenges_dir
        self.template_vars = {
            'Puzzle': '1',  # Default puzzle number
            'ShowObjective': 'true',
            'ShowGraphLabel': 'true'
        }
        self.board_styles = {
            'node_color': 'lightblue',
            'edge_color': 'gray',
            'node_size': 1000,
            'font_size': 10,
            'figsize': (12, 8)
        }
    
    def get_challenge_file(self, challenge_id: str) -> str:
        """Get the correct challenge file path"""
        base_name = f"puzzle{challenge_id.zfill(2)}"
        possible_files = [
            f"{base_name}.gv",
            f"{base_name}-1.gv",
            f"{base_name}-2.gv"
        ]
        
        for file_name in possible_files:
            file_path = os.path.join(self.challenges_dir, file_name)
            if os.path.exists(file_path):
                return file_path
        
        raise FileNotFoundError(f"No challenge file found for puzzle {challenge_id}")
    
    def visualize_challenge(self, challenge_id: str, save_path: str = None):
        """Visualize the challenge as a graph"""
        try:
            # Load and parse the challenge
            file_path = self.get_challenge_file(challenge_id)
            graph_data = self.parse_gv_file(file_path, challenge_id)
            
            # Create NetworkX graph
            G = nx.DiGraph()
            
            # Add nodes
            for node_id, label in graph_data['nodes']:
                if node_id not in ['start', 'objective']:
                    G.add_node(node_id, label=label)
            
            # Add edges
            for src, dst in graph_data['edges']:
                G.add_edge(src, dst)
            
            # Create visualization
            plt.figure(figsize=self.board_styles['figsize'])
            pos = nx.spring_layout(G)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, 
                                 node_color=self.board_styles['node_color'],
                                 node_size=self.board_styles['node_size'])
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, 
                                 edge_color=self.board_styles['edge_color'],
                                 arrows=True)
            
            # Draw labels
            labels = nx.get_node_attributes(G, 'label')
            nx.draw_networkx_labels(G, pos, labels, 
                                  font_size=self.board_styles['font_size'])
            
            plt.title(f"Challenge {challenge_id}")
            plt.axis('off')
            
            if save_path:
                plt.savefig(save_path)
                plt.close()
            else:
                plt.show()
            
            return True
            
        except Exception as e:
            print(f"Error visualizing challenge: {str(e)}")
            return False
    
    def export_challenge_json(self, challenge_id: str, save_path: str):
        """Export challenge data to JSON format"""
        try:
            file_path = self.get_challenge_file(challenge_id)
            graph_data = self.parse_gv_file(file_path, challenge_id)
            board = self.convert_to_board(graph_data)
            
            data = {
                'id': challenge_id,
                'objective': graph_data.get('objective', 'No objective specified'),
                'nodes': graph_data['nodes'],
                'edges': graph_data['edges'],
                'board_state': {
                    'components': [
                        {
                            'type': comp.type.name,
                            'position': comp.position,
                            'state': comp.state if hasattr(comp, 'state') else None
                        }
                        for comp in board.components
                    ]
                }
            }
            
            with open(save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting challenge: {str(e)}")
            return False
    
    def create_challenge_variation(self, base_challenge_id: str, variation_id: str, 
                                 modifications: List[Dict]):
        """Create a variation of an existing challenge"""
        try:
            # Load base challenge
            file_path = self.get_challenge_file(base_challenge_id)
            graph_data = self.parse_gv_file(file_path, base_challenge_id)
            board = self.convert_to_board(graph_data)
            
            # Apply modifications
            for mod in modifications:
                if mod['type'] == 'add_component':
                    board.add_component(
                        ComponentType[mod['component_type']],
                        mod['x'],
                        mod['y']
                    )
                elif mod['type'] == 'remove_component':
                    board.remove_component(mod['x'], mod['y'])
                elif mod['type'] == 'modify_component':
                    board.modify_component(
                        mod['x'],
                        mod['y'],
                        ComponentType[mod['new_type']]
                    )
            
            # Save variation
            variation_path = os.path.join(
                self.challenges_dir,
                f"puzzle{base_challenge_id}-var{variation_id}.gv"
            )
            
            with open(variation_path, 'w') as f:
                f.write(f"digraph Challenge{base_challenge_id}_Var{variation_id} {{\n")
                f.write("    graph [ GRAPH_STYLE ]\n")
                f.write("    node  [ NODE_STYLE  ]\n")
                f.write("    edge  [ EDGE_STYLE  ]\n\n")
                
                # Write nodes
                for comp in board.components:
                    if comp.type != ComponentType.EMPTY:
                        f.write(f'    {comp.type.name}_{comp.position[0]}_{comp.position[1]} '
                               f'[label="{comp.type.name}_{comp.position[0]}_{comp.position[1]}"]\n')
                
                # Write edges
                for comp in board.components:
                    if comp.type != ComponentType.EMPTY:
                        for other in board.components:
                            if other.type != ComponentType.EMPTY:
                                if self._is_connected(comp, other):
                                    f.write(f'    {comp.type.name}_{comp.position[0]}_{comp.position[1]} '
                                           f'-> {other.type.name}_{other.position[0]}_{other.position[1]}\n')
                
                f.write("}\n")
            
            return True
            
        except Exception as e:
            print(f"Error creating challenge variation: {str(e)}")
            return False
    
    def preprocess_gv_file(self, content: str, puzzle_num: str) -> str:
        """Preprocess the GraphViz file by handling preprocessor directives"""
        # Set puzzle number
        self.template_vars['Puzzle'] = puzzle_num
        
        # Handle #if directives
        lines = content.split('\n')
        processed_lines = []
        skip_block = False
        if_stack = []
        
        for line in lines:
            # Handle #if directives
            if line.strip().startswith('#if'):
                condition = line.strip()[3:].strip()
                if 'Puzzle' in condition:
                    # Extract puzzle number from condition
                    match = re.search(r'Puzzle\s*==\s*(\d+)', condition)
                    if match:
                        skip_block = match.group(1) != puzzle_num
                elif condition in self.template_vars:
                    skip_block = self.template_vars[condition].lower() != 'true'
                if_stack.append(skip_block)
                continue
            
            # Handle #elif directives
            if line.strip().startswith('#elif'):
                if if_stack:
                    if_stack.pop()
                condition = line.strip()[5:].strip()
                if 'Puzzle' in condition:
                    match = re.search(r'Puzzle\s*==\s*(\d+)', condition)
                    if match:
                        skip_block = match.group(1) != puzzle_num
                elif condition in self.template_vars:
                    skip_block = self.template_vars[condition].lower() != 'true'
                if_stack.append(skip_block)
                continue
            
            # Handle #endif directives
            if line.strip().startswith('#endif'):
                if if_stack:
                    skip_block = if_stack.pop()
                continue
            
            # Skip lines in false blocks
            if any(if_stack):
                continue
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def parse_gv_file(self, file_path: str, puzzle_num: str) -> Dict:
        """Parse a GraphViz file and extract component information"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Preprocess the file
        processed_content = self.preprocess_gv_file(content, puzzle_num)
        
        # Extract node definitions
        node_pattern = r'(\w+)\s*\[label="([^"]+)"[^\]]*\]'
        nodes = re.findall(node_pattern, processed_content)
        
        # Extract edge definitions
        edge_pattern = r'(\w+)\s*->\s*(\w+)'
        edges = re.findall(edge_pattern, processed_content)
        
        # Extract objective if present
        objective_pattern = r'objective\s*\[[^\]]*label=\$text\(([^)]+)\)'
        objective_match = re.search(objective_pattern, processed_content)
        objective = None
        if objective_match:
            objective = objective_match.group(1)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'objective': objective
        }
    
    def convert_to_board(self, graph_data: Dict) -> GameBoard:
        """Convert GraphViz data to a GameBoard"""
        board = GameBoard()
        
        # Map of component types from GraphViz labels
        component_map = {
            'RAMP': ComponentType.RAMP,
            'GEAR': ComponentType.GEAR,
            'CROSSOVER': ComponentType.CROSSOVER,
            'INTERCEPTOR': ComponentType.INTERCEPTOR,
            'AND': ComponentType.AND_GATE,
            'OR': ComponentType.OR_GATE,
            'BIT': ComponentType.BIT
        }
        
        # Add components based on nodes
        for node_id, label in graph_data['nodes']:
            # Skip special nodes
            if node_id in ['start', 'objective']:
                continue
            
            # Extract component type and position from label
            match = re.match(r'(\w+)_(\d+)_(\d+)', label)
            if match:
                comp_type, x, y = match.groups()
                if comp_type in component_map:
                    board.add_component(
                        component_map[comp_type],
                        int(x),
                        int(y)
                    )
        
        return board
    
    def load_challenge(self, challenge_id: str) -> Tuple[GameBoard, str]:
        """Load a challenge from its GraphViz file"""
        file_path = os.path.join(self.challenges_dir, f"puzzle{challenge_id.zfill(2)}.gv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Challenge file not found: {file_path}")
        
        graph_data = self.parse_gv_file(file_path, challenge_id)
        board = self.convert_to_board(graph_data)
        return board, graph_data.get('objective', 'No objective specified')

def update_challenges_with_gv():
    """Update the challenges dictionary with GraphViz-based challenges"""
    parser = GraphVizParser()
    new_challenges = {}
    
    # Load challenges from GraphViz files
    for i in range(1, 10):  # Assuming we have puzzles 01-09
        try:
            challenge_id = str(i).zfill(2)
            board, objective = parser.load_challenge(challenge_id)
            new_challenges[challenge_id] = {
                "id": challenge_id,
                "board": board,
                "description": f"Puzzle {challenge_id}: {objective}"
            }
        except FileNotFoundError:
            print(f"Warning: Challenge {challenge_id} not found")
            continue
    
    return new_challenges

def run_tests():
    """Run tests for the GraphViz parser"""
    parser = GraphVizParser()
    test_results = {
        'file_loading': [],
        'parsing': [],
        'visualization': [],
        'variations': []
    }
    
    # Test file loading
    for i in range(1, 10):
        try:
            file_path = parser.get_challenge_file(str(i).zfill(2))
            test_results['file_loading'].append((
                f"Challenge {i}",
                os.path.exists(file_path)
            ))
        except Exception as e:
            test_results['file_loading'].append((
                f"Challenge {i}",
                False,
                str(e)
            ))
    
    # Test parsing
    try:
        board, objective = parser.load_challenge("01")
        test_results['parsing'].append((
            "Basic parsing",
            len(board.components) > 0
        ))
    except Exception as e:
        test_results['parsing'].append((
            "Basic parsing",
            False,
            str(e)
        ))
    
    # Test visualization
    try:
        success = parser.visualize_challenge("01", "test_visualization.png")
        test_results['visualization'].append((
            "Basic visualization",
            success
        ))
    except Exception as e:
        test_results['visualization'].append((
            "Basic visualization",
            False,
            str(e)
        ))
    
    # Test variations
    try:
        success = parser.create_challenge_variation(
            "01",
            "1",
            [{
                'type': 'add_component',
                'component_type': 'RAMP',
                'x': 5,
                'y': 5
            }]
        )
        test_results['variations'].append((
            "Basic variation",
            success
        ))
    except Exception as e:
        test_results['variations'].append((
            "Basic variation",
            False,
            str(e)
        ))
    
    # Print results
    print("\nTest Results:")
    for category, results in test_results.items():
        print(f"\n{category.upper()}:")
        for test_name, success, *error in results:
            status = "PASS" if success else "FAIL"
            print(f"  {test_name}: {status}")
            if not success and error:
                print(f"    Error: {error[0]}")

if __name__ == "__main__":
    # Run tests
    run_tests()
    
    # Example usage
    parser = GraphVizParser()
    
    # Visualize a challenge
    parser.visualize_challenge("01", "challenge_01.png")
    
    # Export to JSON
    parser.export_challenge_json("01", "challenge_01.json")
    
    # Create a variation
    parser.create_challenge_variation(
        "01",
        "1",
        [{
            'type': 'add_component',
            'component_type': 'RAMP',
            'x': 5,
            'y': 5
        }]
    )

# Access a GraphViz-based challenge
# challenge = CHALLENGES["01"]  # First puzzle
# print(challenge["description"])  # Will show the objective
# board = challenge["board"] 