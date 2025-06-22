from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import base64
from fastapi.responses import JSONResponse
import json
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize board state
BOARD_SIZE = 8
board_state = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

class PlaceComponentRequest(BaseModel):
    x: int
    y: int
    component: str

class SimulateMarbleRequest(BaseModel):
    start_x: Optional[int] = 7

class SolverPlanRequest(BaseModel):
    pass  # No body needed, uses current board state

class ChallengeRequest(BaseModel):
    challenge_id: str

@app.get('/api/board')
def get_board():
    return {
        'board': board_state,
        'size': BOARD_SIZE
    }

@app.post('/api/board/place')
def place_component(data: PlaceComponentRequest):
    x, y, component = data.x, data.y, data.component
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        board_state[y][x] = component
        return {'success': True, 'board': board_state}
    raise HTTPException(status_code=400, detail='Invalid position')

@app.post('/api/board/simulate')
def simulate_marble(data: SimulateMarbleRequest):
    start_x = data.start_x if data.start_x is not None else 7
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
            pass
        elif component == 'INTERCEPTOR':
            break
            
        y += 1
        
        if x < 0 or x >= BOARD_SIZE:
            break
    return {
        'success': True,
        'path': path,
        'board': board_state
    }

@app.post('/api/solver/plan')
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
        return {
            'success': True,
            'description': solution,
            'steps': steps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/board/reset')
def reset_board():
    global board_state
    board_state = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    return {'success': True, 'board': board_state}

@app.post('/api/solve_puzzle')
async def solve_puzzle(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        image_b64 = base64.b64encode(image_bytes).decode()

        prompt = (
            "This is a Turing Tumble puzzle graph. "
            "1. Extract the puzzle structure and describe it in JSON. "
            "2. Solve the puzzle, and return the solution steps as JSON. "
            "3. Provide performance metrics (simulation speed, accuracy, etc.) as JSON."
        )

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/png;base64,{image_b64}"}
                    ]
                }
            ],
            max_tokens=2048
        )
        result = response.choices[0].message.content
        return JSONResponse(content={"result": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def load_challenge(challenge_path):
    with open(challenge_path, "r") as f:
        data = json.load(f)
    return data["initial_board"], data["goal"], data.get("description", "")

def board_to_text(board):
    return "\n".join(" ".join(row) for row in board)

def parse_board_matrix(text, expected_rows=17, expected_cols=15):
    board = []
    in_board = False
    for line in text.splitlines():
        if not in_board and ("Final Board:" in line or "Board:" in line):
            in_board = True
            continue
        if in_board:
            if len(board) >= expected_rows:
                break
            row = [cell for cell in line.strip().split() if cell]
            if len(row) == expected_cols:
                board.append(row)
    return board

def parse_metrics_table(text):
    metrics = {}
    match = re.search(r"Metric\s+\|\s+Value\n[-\s]+\n((?:.+\|.+\n?)+)", text)
    if not match:
        return metrics
    for line in match.group(1).splitlines():
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 2:
                metrics[parts[0]] = parts[1]
    return metrics

@app.post("/api/solve_challenge")
def solve_challenge(req: ChallengeRequest):
    # 1. Load challenge
    challenge_path = f"TTG_Backend/Challenges/challenge_{req.challenge_id}.json"
    initial_board, goal, description = load_challenge(challenge_path)
    # 2. Format prompt
    prompt = f"""
Turing Tumble Challenge:
Description: {description}
Initial Board:
{board_to_text(initial_board)}
Goal: {goal}
Please solve and provide the final board (17x15) and metrics in the following format:

Final Board:
[...17x15 board here...]

Metric              | Value
---------------------------
Simulation Accuracy | 
State Consistency   | 
Error Rate          | 
Uptime              | 
"""
    # 3. Call GPT-4V
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a Turing Tumble puzzle solver."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048
    )
    gpt4v_output = response.choices[0].message.content
    # 4. Parse output
    board_matrix = parse_board_matrix(gpt4v_output)
    metrics = parse_metrics_table(gpt4v_output)
    # 5. Return as JSON
    return {
        "board": board_matrix,
        "metrics": metrics
    }
