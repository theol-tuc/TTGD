# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

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
        # Simulator functionality removed due to missing ttsim module
        return {
            "status": "error",
            "detail": "Simulator functionality is currently unavailable."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

