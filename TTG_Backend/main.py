# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ttsim.simulator import Simulator

app = FastAPI()

# Define input model
class Cell(BaseModel):
    x: int
    y: int
    type: str
    dir: str = None  # Optional

class BoardData(BaseModel):
    cells: List[Cell]
    width: int
    height: int
    marbles: List[str]

class SimulationRequest(BaseModel):
    board_data: BoardData

@app.post("/simulate")
def simulate(request: SimulationRequest):
    try:
        sim = Simulator()

        # Convert request cells into simulator format
        board_input = {
            "width": request.board_data.width,
            "height": request.board_data.height,
            "cells": [cell.dict() for cell in request.board_data.cells],
            "marbles": request.board_data.marbles
        }

        result = sim.run(board_input)
        return {
            "status": "success",
            "marble_data": result.get("marble_data", []),
            "board": result.get("board", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

