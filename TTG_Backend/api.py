from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, ForwardRef, Any

from game_logic import GameBoard, ComponentType, Marble
from challenges import CHALLENGES, serialize_challenge
import ai_manager
from ai_manager import AIManager
import traceback

# Create a single instance of AIManager
ai_manager = AIManager()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

GameBoardRef = Optional['GameBoard']

# Initialize game board
board = GameBoard(8, 8)


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
    class Config:
        arbitrary_types_allowed = True

    components: List[List[Dict[str, Any]]]
    marbles: List[Dict[str, Any]]
    red_marbles: int
    blue_marbles: int
    active_launcher: str


@app.get("/")
async def root():
    return {"message": "Welcome to Turing Tumble API"}


@app.get("/board")
async def get_board():
    """Get the current state of the board"""
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

    return BoardState(
        components=components,
        marbles=marbles,
        red_marbles=board.red_marbles,
        blue_marbles=board.blue_marbles,
        active_launcher=board.active_launcher
    )


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
    global board
    if not challenge_id:
        raise HTTPException(status_code=422, detail="Missing challenge_id parameter")

    challenge = CHALLENGES.get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    board = challenge["board"]
    return {
        "id": challenge["id"],
        "initialBoard": serialize_challenge(challenge["board"]),
        "red_marbles": challenge["board"].red_marbles,
        "blue_marbles": challenge["board"].blue_marbles,
    }

@app.post("/ai/move")
async def get_ai_move(game_state: Dict[str, Any], challenge_id: str = None):
    """
    Get AI's next move based on current game state and challenge context.
    """
    try:
        move = ai_manager.get_ai_move(game_state, challenge_id)
        return move
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/execute")
async def execute_ai_move(game_state: Dict[str, Any], challenge_id: str = None):
    """
    Execute AI's move and get explanation.
    """
    try:
        move = ai_manager.get_ai_move(game_state, challenge_id)
        explanation = ai_manager.get_ai_explanation(game_state, move, challenge_id)
        return {"move": move, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
