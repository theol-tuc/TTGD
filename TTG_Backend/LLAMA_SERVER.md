# TTG AI System Documentation

## Overview
This documentation covers the AI system implementation used for game component generation in the TTG (Tower of the Gods) project. The system uses a LLaMA 3(pro) model to generate game component placements based on the current game state.

## System Architecture

### 1. `llama_server.py`
The main FastAPI server that hosts the LLaMA model and provides a REST API for generating game components.

#### Code Implementation:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

# Initialize the LLaMA model
model_path = "/home/mtko19/llama-pro-8b-instruct.Q4_K_M.gguf"
llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    verbose=True
)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.3

@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        print("\n=== Debug: Received Request ===")
        print(f"Prompt: {request.prompt}")
        print(f"Max tokens: {request.max_tokens}")
        print(f"Temperature: {request.temperature}")
        
        # Generate response
        response = llm(
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stop=["</s>", "User:", "Assistant:"]
        )
        
        print("\n=== Debug: Raw Model Output ===")
        print(f"Response: {response}")
        
        # Extract the generated text
        output = response["choices"][0]["text"].strip()
        
        print("\n=== Debug: Final Response ===")
        print(f"Output: {output}")
        
        return {"output": output}
    except Exception as e:
        print(f"\n=== Debug: Error ===")
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 2. `ai_manager.py`
Manages the AI system's state and coordinates between different components.

#### Key Responsibilities:
- Manages AI system state
- Coordinates between components
- Handles AI requests and responses
- Maintains game state synchronization

#### Code Implementation:
```python
class AIManager:
    def __init__(self):
        self.game_state = None
        self.board_encoder = BoardEncoder()
        self.ai_service = AIService()

    def update_game_state(self, new_state):
        self.game_state = new_state
        encoded_state = self.board_encoder.encode(new_state)
        return encoded_state

    def get_ai_suggestion(self):
        if not self.game_state:
            raise ValueError("Game state not initialized")
        
        encoded_state = self.board_encoder.encode(self.game_state)
        suggestion = self.ai_service.get_suggestion(encoded_state)
        return suggestion
```

### 3. `ai_service.py`
Handles communication with the LLaMA server and processes AI responses.

#### Key Responsibilities:
- Communicates with LLaMA server
- Processes AI responses
- Handles error cases
- Manages request/response formatting

#### Code Implementation:
```python
class AIService:
    def __init__(self):
        self.server_url = "http://localhost:8001/generate"

    def get_suggestion(self, encoded_state):
        try:
            response = requests.post(
                self.server_url,
                json={
                    "prompt": self._format_prompt(encoded_state),
                    "max_tokens": 512,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                return self._process_response(response.json())
            else:
                raise Exception(f"Server error: {response.text}")
                
        except Exception as e:
            print(f"Error getting AI suggestion: {str(e)}")
            return None
```

### 4. `board_encoder.py`
Encodes and decodes game board states for AI processing.

#### Key Responsibilities:
- Encodes game state for AI processing
- Decodes AI responses into game actions
- Maintains board state representation
- Handles board state validation

#### Code Implementation:
```python
class BoardEncoder:
    def __init__(self):
        self.board_size = (5, 5)
        self.component_types = {
            "RAMP_LEFT": 1,
            "RAMP_RIGHT": 2,
            "PLATFORM": 3
        }

    def encode(self, game_state):
        # Convert game state to AI-readable format
        encoded = {
            "board_size": self.board_size,
            "components": self._encode_components(game_state.components),
            "available": game_state.available_components
        }
        return encoded

    def decode(self, ai_response):
        # Convert AI response to game action
        return self._parse_action(ai_response)
```

### 5. `game_state.py`
Manages the current state of the game.

#### Key Responsibilities:
- Tracks current game state
- Manages component placements
- Validates moves
- Updates game progress

#### Code Implementation:
```python
class GameState:
    def __init__(self):
        self.board_size = (5, 5)
        self.components = []
        self.available_components = []
        self.goal = None

    def add_component(self, component_type, x, y):
        if self._is_valid_placement(component_type, x, y):
            self.components.append({
                "type": component_type,
                "x": x,
                "y": y
            })
            return True
        return False

    def _is_valid_placement(self, component_type, x, y):
        # Validate component placement
        return True  # Implementation details
```

## Setup Instructions

1. **SSH Tunnel Setup**:
   ```bash
   ssh -L 8001:localhost:8001 mtko19@cloud-247.rz.tu-clausthal.de
   ```

2. **Start the Server**:
   ```bash
   python llama_server.py
   ```

3. **Run Tests**:
   ```bash
   python test_llm_connection.py
   ```

## Error Handling

The system implements comprehensive error handling:
- Connection errors
- Model loading failures
- Invalid requests
- Empty responses
- Game state validation
- Component placement validation

## Debug Output

The system provides detailed debug output:
- Model loading confirmation
- Received prompts
- Raw model output
- Final processed response
- Game state changes
- Component placements
- Any errors encountered

## Notes
- The server must be running on the remote machine
- Local access is provided through SSH tunnel
- The model path is hardcoded to the server's model location
- Default parameters can be adjusted in the `GenerateRequest` class
- Game state must be properly initialized before AI suggestions
- Component placements must be validated before application 