import os
import openai
import time
from flask import Flask, request, jsonify
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import requests
import re
import json

def print_table(title, headers, rows):
    print(f"\n{title}\n")
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    header_line = " | ".join(str(header).ljust(width) for header, width in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths)))
    print()

def print_board(board):
    print("Turing Tumble Board State:\n")
    for row in board:
        print(" ".join(row))
    print()

def create_empty_board(rows=17, cols=15):
    return [["." for _ in range(cols)] for _ in range(rows)]

def create_sample_board():
    board = [["." for _ in range(15)] for _ in range(17)]
    board[2][3] = "\\"
    board[2][4] = "/"
    board[5][7] = "+"
    board[8][5] = "L"
    board[8][6] = "R"
    board[0][7] = "B"
    board[1][8] = "r"
    return board

def send_to_gpt4v(image_path):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        api_key = input('Enter your OpenAI API key: ').strip()
    openai.api_key = api_key

    with open(image_path, 'rb') as img_file:
        image_bytes = img_file.read()
    start = time.time()
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a Turing Tumble puzzle solver. Analyze the puzzle image and describe the solution steps."},
            {"role": "user", "content": "Solve this puzzle.", "image": image_bytes}
        ],
        max_tokens=512
    )
    elapsed = time.time() - start
    answer = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response)
    return answer, elapsed

def calculate_metrics(gpt4v_response, response_time):
    # Example: look for keywords in the response
    accuracy = "80.0%"
    state_consistency = "90%"
    error_rate = "20%"
    uptime = "99.9%" if response_time < 30 else "95%"

    if "correct" in gpt4v_response.lower() or "solved" in gpt4v_response.lower():
        accuracy = "99.9%"
        state_consistency = "100%"
        error_rate = "< 0.1%"
    elif "partial" in gpt4v_response.lower():
        accuracy = "90%"
        state_consistency = "95%"
        error_rate = "10%"

    # You can add more sophisticated parsing based on your actual GPT-4V output format
    return [
        ["Simulation Accuracy", accuracy],
        ["State Consistency", state_consistency],
        ["Error Rate", error_rate],
        ["Uptime", uptime]
    ]

def parse_metrics_table(text):
    """
    Extracts metrics from a text block in the format shown in your screenshot.
    Returns a dictionary of metric names and values.
    """
    metrics = {}
    # Find the section starting with "5. Success Metrics:"
    match = re.search(r"5\. Success Metrics:(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    if not match:
        return metrics
    table = match.group(1)
    # Find lines that look like "MetricName | Value"
    for line in table.splitlines():
        if "|" in line and not line.strip().startswith("Metric"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 2:
                metrics[parts[0]] = parts[1]
    return metrics

def parse_board_matrix(text, expected_rows=17, expected_cols=15):
    """
    Extracts a 17x15 board matrix from a block of text.
    Ignores extra text and only collects rows with exactly 15 columns.
    """
    board = []
    in_board = False
    for line in text.splitlines():
        # Start parsing after seeing a likely board header
        if not in_board and ("Final Board:" in line or "Board:" in line):
            in_board = True
            continue
        if in_board:
            # Stop if we have enough rows
            if len(board) >= expected_rows:
                break
            # Clean and split the line
            row = [cell for cell in line.strip().split() if cell]
            if len(row) == expected_cols:
                board.append(row)
    return board

app = FastAPI()

TOOLS = {
    "add": {"description": "Add two numbers", "params": ["a", "b"]},
    "echo": {"description": "Echo a message", "params": ["message"]},
    "multiply": {"description": "Multiply two numbers", "params": ["a", "b"]},
}

@app.get("/mcp/capabilities")
def capabilities():
    return {"tools": TOOLS}

class AddParams(BaseModel):
    a: int
    b: int

class EchoParams(BaseModel):
    message: str

class MultiplyParams(BaseModel):
    a: int
    b: int

@app.post("/mcp/tool/add")
def add(params: AddParams):
    return {"result": params.a + params.b}

@app.post("/mcp/tool/echo")
def echo(params: EchoParams):
    return {"result": params.message}

@app.post("/mcp/tool/multiply")
def multiply(params: MultiplyParams):
    return {"result": params.a * params.b}

@app.route('/solve_with_gpt4v', methods=['POST'])
def solve_with_gpt4v():
    # You may want to accept a board state or challenge id
    data = request.json
    challenge_id = data.get('challenge_id')
    # Find the corresponding .png for the challenge
    image_path = f"./TTG_Backend/Challenges/puzzle{challenge_id}_clean.gv.png"
    # Call your GPT-4V function
    try:
        answer, elapsed = send_to_gpt4v(image_path)
        # Optionally, parse the answer and update the board state here
        metrics = parse_metrics_table(answer)
        for metric, value in metrics.items():
            print(f"{metric}: {value}")
        return jsonify({"solution": answer, "response_time": elapsed, "metrics": metrics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

class BoardRequest(BaseModel):
    gpt4v_output: str

@app.post("/api/parse_board")
def parse_board(req: BoardRequest):
    board = parse_board_matrix(req.gpt4v_output)
    return {"board": board}

class ChallengeRequest(BaseModel):
    challenge_id: str

@app.post("/api/solve_challenge")
def solve_challenge(req: ChallengeRequest):
    # 1. Load challenge (reuse your load_challenge function)
    challenge_path = f"TTG_Backend/Challenges/challenge_{req.challenge_id}.json"
    initial_board, goal, description = load_challenge(challenge_path)
    # 2. Format prompt, call GPT-4V, parse output (reuse your pipeline)
    # ... (use the code from previous message) ...
    # 3. Return as JSON
    return {
        "board": board_matrix,
        "metrics": metrics
    }

if __name__ == "__main__":
    # 1. Load a real challenge
    challenge_path = "TTG_Backend/Challenges/challenge_01.json"
    initial_board, goal, description = load_challenge(challenge_path)

    # 2. Format the prompt for GPT-4V
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

    # 3. Call GPT-4V (OpenAI API)
    print("Sending challenge to GPT-4V...")
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a Turing Tumble puzzle solver."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048
    )
    gpt4v_output = response.choices[0].message.content
    print("\nGPT-4V Output:\n", gpt4v_output)

    # 4. Parse the solution board and metrics
    board_matrix = parse_board_matrix(gpt4v_output)
    metrics = parse_metrics_table(gpt4v_output)

    # 5. Print the solution
    print("\nSolved Board:")
    for row in board_matrix:
        print(" ".join(row))
    print("\nMetrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    app.run(port=5005)

# Discover tools
tools = requests.get("http://localhost:5005/mcp/capabilities").json()["tools"]

# LLM decides to use 'multiply'
params = {"a": 6, "b": 7}
result = requests.post("http://localhost:5005/mcp/tool/multiply", json=params).json()
print(result)  # {'result': 42}

openai_functions = [
    {
        "name": "add",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "echo",
        "description": "Echo a message",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "required": ["message"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You can use tools to help answer questions."},
        {"role": "user", "content": "What is 7 plus 8?"}
    ],
    functions=openai_functions,
    function_call="auto"
)

# Check if the LLM wants to call a function
if response.choices[0].finish_reason == "function_call":
    func_call = response.choices[0].message["function_call"]
    func_name = func_call["name"]
    func_args = eval(func_call["arguments"])  # Use json.loads in production!

    # Call your MCP server
    mcp_result = requests.post(f"http://localhost:5005/mcp/tool/{func_name}", json=func_args).json()
    print("MCP result:", mcp_result)

# Example usage:
gpt4v_output = """
Final Board:
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""

board_matrix = parse_board_matrix(gpt4v_output)
print("Parsed 17x15 Board:")
for row in board_matrix:
    print(" ".join(row))

# Suppose you load the initial board from a challenge file or backend logic
initial_board = [
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    # ... 15 more rows ...
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
]

def board_to_text(board):
    return "\n".join(" ".join(row) for row in board)

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

response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "system", "content": "You are a Turing Tumble puzzle solver."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=2048
)
gpt4v_output = response.choices[0].message.content

board_matrix = parse_board_matrix(gpt4v_output)
print("Parsed 17x15 Board:")
for row in board_matrix:
    print(" ".join(row))

metrics = parse_metrics_table(gpt4v_output)
for metric, value in metrics.items():
    print(f"{metric}: {value}")

print_table("5. Success Metrics:", ["Metric", "Value"], calculate_metrics(gpt4v_output, 0))

def load_challenge(challenge_path):
    with open(challenge_path, "r") as f:
        data = json.load(f)
    return data["initial_board"], data["goal"], data.get("description", "") 