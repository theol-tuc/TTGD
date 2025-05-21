from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import subprocess
import json
import os
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str
    board_state: Dict[str, Any]


class ExplainRequest(BaseModel):
    prompt: str
    board_state: Dict[str, Any]
    move: Dict[str, Any]


def extract_json(response_text: str) -> str:
    """Extract the first valid JSON object from the response text."""
    # First try to find a complete JSON object
    match = re.search(r'\{[^{}]*\}', response_text)
    if match:
        try:
            # Validate that it's actually JSON
            json.loads(match.group(0))
            return match.group(0)
        except json.JSONDecodeError:
            pass

    # If no valid JSON found, return None
    return None


def call_llm(prompt: str) -> str:
    """Call the LLM server with the given prompt."""
    try:
        # Create a temporary script with the prompt
        script_content = f"""#!/bin/bash
export PYTHONUSERBASE=/tmp/mtko19/python-lib
export PATH=$PYTHONUSERBASE/bin:$PATH
export PYTHONPATH=$PYTHONUSERBASE/lib/python3.12/site-packages:$PYTHONPATH
export PIP_CACHE_DIR=/tmp/mtko19/pip-cache

cd /tmp/mtko19/llama.cpp/build
PROMPT="{prompt}"
./bin/llama-cli -m /tmp/mtko19/models/llama-2-13b-chat/llama-2-13b-chat.Q4_K_M.gguf -p "$PROMPT" -n 200
"""

        # Write the script to a temporary file
        with open("temp_llama.sh", "w") as f:
            f.write(script_content)

        # Make it executable
        os.chmod("temp_llama.sh", 0o755)

        # Run the script and capture output
        result = subprocess.run(
            ["bash", "temp_llama.sh"],
            capture_output=True,
            text=True
        )

        # Clean up
        os.remove("temp_llama.sh")

        if result.returncode != 0:
            raise Exception(f"LLAMA error: {result.stderr}")

        # Extract the response (everything after the prompt)
        response = result.stdout.split(prompt)[-1].strip()
        return response

    except Exception as e:
        raise Exception(f"Error calling LLM: {str(e)}")


@app.post("/generate")
async def generate_move(request: GenerateRequest):
    try:
        # Format the prompt for the LLM
        formatted_prompt = f"""
{request.prompt}

Current board state:
{json.dumps(request.board_state, indent=2)}

Please provide a move in the following JSON format:
{{
    "action": "add_component",
    "parameters": {{
        "type": "<component_type>",
        "x": <x_coordinate>,
        "y": <y_coordinate>
    }},
    "explanation": "<explanation>",
    "text_representation": "<human_readable_description>"
}}

Your response should be a valid JSON object following the format above.
"""

        # Call the LLM
        response = call_llm(formatted_prompt)

        # Extract and validate JSON
        json_str = extract_json(response)
        if not json_str:
            raise HTTPException(status_code=500, detail="No valid JSON found in LLM response")

        try:
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON in LLM response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def explain_move(request: ExplainRequest):
    try:
        # Format the prompt for the LLM
        formatted_prompt = f"""
{request.prompt}

Current board state:
{json.dumps(request.board_state, indent=2)}

Move to explain:
{json.dumps(request.move, indent=2)}

Please provide an explanation for this move in the following JSON format:
{{
    "explanation": "<detailed_explanation_of_the_move>"
}}

Your response should be a valid JSON object following the format above.
"""

        # Call the LLM
        response = call_llm(formatted_prompt)

        # Extract and validate JSON
        json_str = extract_json(response)
        if not json_str:
            raise HTTPException(status_code=500, detail="No valid JSON found in LLM response")

        try:
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON in LLM response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)