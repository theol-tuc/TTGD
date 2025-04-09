from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from game_logic import GameBoard, ComponentType

app = FastAPI()

# Initialize game board
game_board = GameBoard(width=8, height=8)  # You can adjust the size as needed


class Position(BaseModel):
    x: int
    y: int


class ComponentRequest(BaseModel):
    type: int  # ComponentType value
    x: int
    y: int


class LauncherRequest(BaseModel):
    launcher_index: int


@app.post("/add_component")
async def add_component(component: ComponentRequest):
    try:
        component_type = ComponentType(component.type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid component type")

    success = game_board.add_component(component_type, component.x, component.y)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid position")
    return {"message": "Component added successfully"}


@app.post("/launch_marble")
async def launch_marble(request: LauncherRequest):
    success = game_board.launch_marble(request.launcher_index)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid launcher index")
    return {"message": "Marble launched successfully"}


@app.post("/update_physics")
async def update_physics():
    """Update all marble positions based on physics and components"""
    game_board.update_marble_positions()
    return {"message": "Physics updated successfully"}


@app.get("/board_state")
async def get_board_state():
    return {
        "board": game_board.get_board_state(),
        "marbles": game_board.get_marble_positions(),
        "components": game_board.get_component_positions()
    }