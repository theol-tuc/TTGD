# Turing Tumble Backend

This is a backend implementation for the Turing Tumble game that simulates marble movement and component interactions.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn api:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Add a Component
- **POST** `/add_component`
- Body: `{"type": 2, "x": 0, "y": 0}`
- Component Types:
  - 0: EMPTY
  - 1: MARBLE
  - 2: RAMP_LEFT (blue ramp)
  - 3: RAMP_RIGHT (red ramp)
  - 4: CROSSOVER
  - 5: INTERCEPTOR
  - 6: LAUNCHER

### Launch a Marble
- **POST** `/launch_marble`
- Body: `{"launcher_index": 0}`
- Launches a marble from the specified launcher

### Update Physics
- **POST** `/update_physics`
- Updates all marble positions based on components and physics

### Get Board State
- **GET** `/board_state`
- Returns:
  - Current board state
  - Positions of all marbles
  - Positions and types of all components

## Example Usage

1. Add a blue ramp (left):
```bash
curl -X POST "http://localhost:8000/add_component" -H "Content-Type: application/json" -d '{"type": 2, "x": 3, "y": 2}'
```

2. Add a red ramp (right):
```bash
curl -X POST "http://localhost:8000/add_component" -H "Content-Type: application/json" -d '{"type": 3, "x": 4, "y": 2}'
```

3. Add a launcher:
```bash
curl -X POST "http://localhost:8000/add_component" -H "Content-Type: application/json" -d '{"type": 6, "x": 0, "y": 0}'
```

4. Launch a marble:
```bash
curl -X POST "http://localhost:8000/launch_marble" -H "Content-Type: application/json" -d '{"launcher_index": 0}'
```

5. Update physics (marble movement):
```bash
curl -X POST "http://localhost:8000/update_physics"
```

6. Get current board state:
```bash
curl "http://localhost:8000/board_state"
``` 