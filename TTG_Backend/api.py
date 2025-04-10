from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional, ForwardRef
from game_logic import GameBoard, ComponentType, Marble

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
board = GameBoard()

class ComponentRequest(BaseModel):
    type: str
    x: int
    y: int

class MarbleRequest(BaseModel):
    color: str
    x: Optional[int] = None
    y: Optional[int] = None

class BoardState(BaseModel):
    #maybe remove this line later:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    components: List[List[Dict[str, any]]]
    marbles: List[Dict[str, any]]
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
            board.marbles.append(Marble(marble.color, marble.x, marble.y))
            board.components[marble.y][marble.x].is_occupied = True
            return {"message": "Marble added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Position is occupied")
    else:
        # Launch marble from active launcher
        board.launch_marble(marble.color)
        return {"message": "Marble launched successfully"}

@app.post("/launcher")
async def set_launcher(launcher: str):
    """Set the active launcher"""
    if launcher not in ["left", "right"]:
        raise HTTPException(status_code=400, detail="Invalid launcher type")
    board.set_active_launcher(launcher)
    return {"message": f"Launcher set to {launcher}"}

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

#maybe remove this line later:
BoardState.model_rebuild(GameBoard=GameBoard)