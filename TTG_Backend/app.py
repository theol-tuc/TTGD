from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize board state
BOARD_SIZE = 8
board_state = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

@app.route('/api/board', methods=['GET'])
def get_board():
    return jsonify({
        'board': board_state,
        'size': BOARD_SIZE
    })

@app.route('/api/board/place', methods=['POST'])
def place_component():
    data = request.json
    x, y = data['x'], data['y']
    component = data['component']
    
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        board_state[y][x] = component
        return jsonify({'success': True, 'board': board_state})
    return jsonify({'success': False, 'error': 'Invalid position'}), 400

@app.route('/api/board/simulate', methods=['POST'])
def simulate_marble():
    data = request.json
    start_x = data.get('start_x', 7)  # Default to rightmost column
    
    # Simple simulation logic
    path = []
    x, y = start_x, 0
    
    while y < BOARD_SIZE:
        path.append({'x': x, 'y': y})
        component = board_state[y][x]
        
        if component == 'RAMP_LEFT':
            x -= 1
        elif component == 'RAMP_RIGHT':
            x += 1
        elif component == 'CROSSOVER':
            # In a real implementation, this would be more complex
            pass
        elif component == 'INTERCEPTOR':
            break
            
        y += 1
        
        if x < 0 or x >= BOARD_SIZE:
            break
    
    return jsonify({
        'success': True,
        'path': path,
        'board': board_state
    })

@app.route('/api/solver/plan', methods=['POST'])
def get_solution():
    try:
        # Convert board state to a format GPT-4 can understand
        board_description = "Current board state:\n"
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                component = board_state[y][x]
                if component:
                    board_description += f"Position ({x},{y}): {component}\n"
        
        # Get solution from GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Turing Tumble puzzle solver. Analyze the board state and provide a solution."},
                {"role": "user", "content": f"{board_description}\n\nPlease provide a solution to complete this puzzle."}
            ]
        )
        
        solution = response.choices[0].message.content
        
        # Parse the solution into steps
        steps = []
        for line in solution.split('\n'):
            if ':' in line:
                step = line.split(':', 1)[1].strip()
                steps.append(step)
        
        return jsonify({
            'success': True,
            'description': solution,
            'steps': steps
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/board/reset', methods=['POST'])
def reset_board():
    global board_state
    board_state = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    return jsonify({'success': True, 'board': board_state})

if __name__ == '__main__':
    app.run(debug=True)
