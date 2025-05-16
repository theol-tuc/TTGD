from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, ForwardRef, Any
import TTG_Backend.AIChallengeSolver as AIChallengeSolver
from TTG_Backend.game_logic import GameBoard, ComponentType, Marble
from TTG_Backend.challenges import CHALLENGES, serialize_challenge
from TTG_Backend.AIChallengeSolver import TransformerPlanner
import uvicorn
from .solver import setup_challenge, run_solver

import numpy as np

app = FastAPI(title="Turing Tumble AI Solver API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

GameBoardRef = Optional['GameBoard']

# Initialize game board and AI manager
board = GameBoard(red=3, blue=3)  # Initialize with 3 red and 3 blue marbles

# Persistent in-memory board state
PERSISTENT_BOARD = [['.' for _ in range(15)] for _ in range(17)]

class ComponentRequest(BaseModel):
    type: str
    x: int
    y: int

class MarbleRequest(BaseModel):
    color: str
    x: Optional[int] = None
    y: Optional[int] = None

class LauncherRequest(BaseModel):
    launcher: str

class BoardState(BaseModel):
    components: List[Dict[str, Any]]
    marble_color: str = "blue"

class SolverResponse(BaseModel):
    plan: List[Dict[str, Any]]
    board_state: Dict[str, Any]

class BoardRequest(BaseModel):
    board: List[List[str]]

class DropMarbleRequest(BaseModel):
    board: List[List[str]]
    side: str  # 'left' or 'right'

class ResetBoardResponse(BaseModel):
    board: List[List[str]]

class DropMarbleResponse(BaseModel):
    board: List[List[str]]
    path: List[List[int]]  # List of [row, col] positions the marble passed through

class SetBoardRequest(BaseModel):
    board: List[List[str]]

@app.get("/")
async def root():
    return {"message": "Turing Tumble AI Solver API"}

@app.get("/board")
async def get_board():
    return {"board": PERSISTENT_BOARD}

@app.post("/set-board")
async def set_board(request: SetBoardRequest):
    global PERSISTENT_BOARD
    PERSISTENT_BOARD = [row[:] for row in request.board]
    return {"message": "Board updated"}

@app.post("/components")
async def add_component(component: ComponentRequest):
    """Add a component to the board"""
    try:
        component_type = ComponentType(component.type)
        board.add_component(component_type, component.x, component.y)
        return {"message": "Component added successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid component type")

@app.post("/marbles")
async def add_marble(marble: MarbleRequest):
    """Add a marble to the board"""
    if marble.x is not None and marble.y is not None:
        # Add marble at specific position
        if not board.check_collision(marble.x, marble.y):
            board.marbles.append(Marble(marble.color, marble.x, marble.y, "right"))  # Default direction
            board.components[marble.y][marble.x].is_occupied = True
            return {"message": "Marble added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Position is occupied")
    else:
        # Launch marble from active launcher
        board.launch_marble(marble.color)
        return {"message": "Marble launched successfully"}

@app.get("/output")
async def get_outputs():
    """Get the marble outputs"""
    return board.get_marble_output()

@app.post("/launcher")
async def set_launcher(launcher_request: LauncherRequest):
    """Set the active launcher"""
    if launcher_request.launcher not in ["left", "right"]:
        raise HTTPException(status_code=400, detail="Invalid launcher type")
    board.set_active_launcher(launcher_request.launcher)
    return {"message": f"Launcher set to {launcher_request.launcher}"}

@app.post("/update")
async def update_board():
    """Update the board state"""
    board.update_marble_positions()
    return {"message": "Board updated successfully"}

@app.post("/reset")
async def reset_board():
    """Reset the board"""
    board.reset()
    return {"message": "Board reset successfully"}

@app.get("/counts")
async def get_counts():
    """Get marble counts"""
    return board.get_marble_counts()

@app.get("/challenge_id")
async def get_challenge(challenge_id: str):
    """Get a specific challenge"""
    if not challenge_id:
        raise HTTPException(status_code=422, detail="Missing challenge_id parameter")
    
    challenge = CHALLENGES.get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    return {
        "id": challenge["id"],
        "initialBoard": serialize_challenge(challenge["board"]),
        "red_marbles": challenge["board"].red_marbles,
        "blue_marbles": challenge["board"].blue_marbles
    }

@app.post("/ai/move")
async def get_ai_move():
    """Get AI's next move based on current game state"""
    try:
        # Get current board state
        components = []
        for row in board.components:
            component_row = []
            for component in row:
                component_row.append({
                    "type": component.type.value,
                    "is_occupied": component.is_occupied
                })
            components.append(component_row)
        
        marbles = []
        for marble in board.marbles:
            marbles.append({
                "color": marble.color,
                "x": marble.x,
                "y": marble.y,
                "direction": marble.direction,
                "is_moving": marble.is_moving
            })
        
        game_state = {
            "components": components,
            "marbles": marbles,
            "red_marbles": board.red_marbles,
            "blue_marbles": board.blue_marbles,
            "active_launcher": board.active_launcher
        }
        
        # Get AI move
        ai_move = AIChallengeSolver.get_ai_move(game_state)
        if not ai_move:
            raise HTTPException(status_code=500, detail="Failed to get AI move")
        
        # Get AI explanation
        explanation = AIChallengeSolver.get_ai_explanation(game_state, ai_move)
        
        return {
            "move": ai_move,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/execute")
async def execute_ai_move():
    """Execute the AI's move"""
    try:
        # Get AI move
        components = []
        for row in board.components:
            component_row = []
            for component in row:
                component_row.append({
                    "type": component.type.value,
                    "is_occupied": component.is_occupied
                })
            components.append(component_row)
        
        marbles = []
        for marble in board.marbles:
            marbles.append({
                "color": marble.color,
                "x": marble.x,
                "y": marble.y,
                "direction": marble.direction,
                "is_moving": marble.is_moving
            })
        
        game_state = {
            "components": components,
            "marbles": marbles,
            "red_marbles": board.red_marbles,
            "blue_marbles": board.blue_marbles,
            "active_launcher": board.active_launcher
        }
        
        ai_move = AIChallengeSolver.get_ai_move(game_state)
        if not ai_move:
            raise HTTPException(status_code=500, detail="Failed to get AI move")
        
        # Execute the move
        action = ai_move["action"]
        parameters = ai_move["parameters"]
        
        if action == "add_component":
            component_type = ComponentType(parameters["type"])
            board.add_component(component_type, parameters["x"], parameters["y"])
        elif action == "launch_marble":
            board.launch_marble(parameters["color"])
        elif action == "set_launcher":
            board.set_active_launcher(parameters["launcher"])
        else:
            raise HTTPException(status_code=400, detail="Invalid AI move action")
        
        return {"message": "AI move executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def simulate_marble_drop(board: List[List[str]], side: str):
    board_array = np.array(board)
    start_col = 2 if side == 'left' else len(board_array[0]) - 3
    current_row = 0
    current_col = start_col
    direction = 0
    path = [[current_row, current_col]]
    while current_row < len(board_array) - 1:
        current_cell = board_array[current_row][current_col]
        if current_cell == '\\':
            direction = -1
        elif current_cell == '/':
            direction = 1
        elif current_cell == '+':
            direction = 0
        elif current_cell == 'X':
            break
        elif current_cell == '<':
            direction = -1
            board_array[current_row][current_col] = '>'
        elif current_cell == '>':
            direction = 1
            board_array[current_row][current_col] = '<'
        elif current_cell == 'G':
            direction = 0
        else:
            direction = 0
        current_row += 1
        current_col += direction
        if current_col < 0 or current_col >= len(board_array[0]):
            break
        path.append([current_row, current_col])
    if 0 <= current_row < len(board_array) and 0 <= current_col < len(board_array[0]):
        board_array[current_row][current_col] = 'O'
    return board_array.tolist(), path

@app.post("/drop-marble", response_model=DropMarbleResponse)
async def drop_marble(request: DropMarbleRequest):
    try:
        result_board, path = simulate_marble_drop(request.board, request.side)
        global PERSISTENT_BOARD
        PERSISTENT_BOARD = [row[:] for row in result_board]
        return {"board": result_board, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-board", response_model=ResetBoardResponse)
async def reset_board():
    try:
        global PERSISTENT_BOARD
        PERSISTENT_BOARD = [['.' for _ in range(15)] for _ in range(17)]
        return {"board": PERSISTENT_BOARD}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solve", response_model=SolverResponse)
async def solve_challenge(board_state: BoardState):
    try:
        # Initialize the board
        board = GameBoard()
        
        # Set up components from the request
        for comp in board_state.components:
            x, y = comp["position"]
            comp_type = ComponentType[comp["type"]]
            board.set_component(x, y, comp_type)
        
        # Initialize the solver
        planner = TransformerPlanner()
        
        # Get the solution
        solution = planner.plan(board_state.marble_color)
        
        # Parse the solution into steps
        steps = planner.parse_plan(solution)
        
        # Convert steps to response format
        plan = [
            {
                "type": step[0].name,
                "position": [step[1], step[2]]
            }
            for step in steps
        ]
        
        return SolverResponse(
            plan=plan,
            board_state={
                "components": board_state.components,
                "marble_color": board_state.marble_color
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_solver():
    try:
        run_solver()
        return {"message": "Test completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
