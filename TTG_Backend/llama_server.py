from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import os
import re
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
LLAMA_CLI_PATH = "/tmp/mtko19/llama.cpp/build/bin/llama-cli"
LOG_DIR = "/tmp/mtko19/llama_logs"

class GenerateRequest(BaseModel):
    prompt: str


def extract_json(raw_output: str) -> dict:
    """
    Extract and validate JSON from LLM output using multiple strategies.
    Returns the first valid JSON object that matches our expected format.
    """
    # Log raw output to file for debugging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"llama_output_{timestamp}.txt")
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== Raw LLM Output ===\n")
        f.write(raw_output)
        f.write("\n=== End Raw Output ===\n")

    # Strategy 1: Look for JSON between delimiters
    delimiter_match = re.search(r"\[START_JSON\](.*?)\[END_JSON\]", raw_output, re.DOTALL)
    if delimiter_match:
        try:
            json_str = delimiter_match.group(1).strip()
            parsed = json.loads(json_str)
            if all(k in parsed for k in ["action", "parameters", "explanation"]):
                return parsed
        except json.JSONDecodeError:
            pass

    # Strategy 2: Find all JSON-like objects
    json_matches = re.findall(r"{[^{}]*}", raw_output)
    for json_str in json_matches:
        try:
            parsed = json.loads(json_str)
            if all(k in parsed for k in ["action", "parameters", "explanation"]):
                return parsed
        except json.JSONDecodeError:
            continue

    # Strategy 3: Look for the largest JSON object
    large_json_match = re.search(r"{.*}", raw_output, re.DOTALL)
    if large_json_match:
        try:
            json_str = large_json_match.group(0)
            parsed = json.loads(json_str)
            if all(k in parsed for k in ["action", "parameters", "explanation"]):
                return parsed
        except json.JSONDecodeError:
            pass

    return None


@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        # Verify llama-cli exists
        if not os.path.exists(LLAMA_CLI_PATH):
            raise HTTPException(
                status_code=500,
                detail=f"llama-cli not found at {LLAMA_CLI_PATH}"
            )

        # Run llama-cli with the prompt
        process = subprocess.Popen(
            [LLAMA_CLI_PATH, "generate", "--prompt", request.prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"[LLaMA Error] {stderr}")
            raise HTTPException(status_code=500, detail=f"LLaMA process error: {stderr}")

        # Extract and validate JSON
        parsed_json = extract_json(stdout)
        if parsed_json:
            return {"response": parsed_json}
        else:
            raise HTTPException(
                status_code=500, 
                detail="No valid JSON found in LLM response. Check llama_logs directory for raw output."
            )

    except Exception as e:
        print(f"[LLaMA Server Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)