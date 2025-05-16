from flask import Flask, request, jsonify
from flask_cors import CORS
from TTG_Backend.game_logic import GameBoard, ComponentType, BLUE
from TTG_Backend.board_encoder import BoardEncoder
from TTG_Backend.AIChallengeSolver import TransformerPlanner

app = Flask(__name__)
CORS(app)

# Initialize components
board = GameBoard()
encoder = BoardEncoder()
planner = TransformerPlanner()

@app.route('/api/board/state', methods=['GET'])
def get_board_state():
    """Get current board state"""
    return jsonify({
        'board': board.get_board_state(),
        'outputs': board.outputs
    })

@app.route('/api/board/component', methods=['POST'])
def place_component():
    """Place a component on the board"""
    data = request.json
    x, y = data['x'], data['y']
    component_type = ComponentType[data['type']]
    board.set_component(x, y, component_type)
    return jsonify({'success': True})

@app.route('/api/board/drop', methods=['POST'])
def drop_marble():
    """Drop a marble at specified position"""
    data = request.json
    x = data['x']
    board.drop_marble(x, BLUE)
    return jsonify({
        'success': True,
        'outputs': board.outputs
    })

@app.route('/api/solver/plan', methods=['POST'])
def get_solution_plan():
    """Get AI solution plan for current board state"""
    encoded_state = encoder.encode_board(board)
    plan = planner.plan(encoded_state)
    steps = planner.parse_plan(plan)
    return jsonify({
        'plan': plan,
        'steps': steps
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
