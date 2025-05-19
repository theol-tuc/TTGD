from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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


@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        # Create a temporary script with the prompt
        script_content = f"""#!/bin/bash
export PYTHONUSERBASE=/tmp/mtko19/python-lib
export PATH=$PYTHONUSERBASE/bin:$PATH
export PYTHONPATH=$PYTHONUSERBASE/lib/python3.12/site-packages:$PYTHONPATH
export PIP_CACHE_DIR=/tmp/mtko19/pip-cache

cd /tmp/mtko19/llama.cpp/build
PROMPT="{request.prompt}"
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
            raise HTTPException(status_code=500, detail=f"LLAMA error: {result.stderr}")

        # Extract the response (everything after the prompt)
        response = result.stdout.split(request.prompt)[-1].strip()

        # Try to extract and validate JSON
        json_str = extract_json(response)
        if json_str:
            try:
                parsed_json = json.loads(json_str)
                return {"response": parsed_json}
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid JSON in LLM response")
        else:
            raise HTTPException(status_code=500, detail="No valid JSON found in LLM response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)