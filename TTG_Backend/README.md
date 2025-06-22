# Turing Tumble AI Solver Backend

## Overview

This backend provides an API for solving Turing Tumble challenges using OpenAI GPT-4V. It loads challenge definitions, formats prompts, sends them to GPT-4V, parses the AI's solution and metrics, and exposes the results via a REST API.

---

## Features

- **Challenge Management:**  
  Store and load challenge definitions (board, goal, description) as JSON files in `TTG_Backend/Challenges/`.

- **AI Integration:**  
  - Formats board state and challenge goal as a prompt.
  - Sends prompt to GPT-4V using the OpenAI API.
  - Parses the returned solution board (17x15) and performance metrics.

- **REST API:**  
  - `/api/solve_challenge`: Accepts a challenge ID, runs the AI solver, and returns the solved board and metrics as JSON.

---

## Directory Structure

```
TTG_Backend/
├── app.py                # FastAPI app with API endpoints
├── ttg_demo.py           # Script for local testing/demo
├── Challenges/
│   ├── challenge_01.json # Example challenge file
│   └── ...               # More challenge files
├── game_logic.py         # (If used) Board logic
├── game_state.py         # (If used) Board state serialization
└── ...                   # Other backend files
```

---

## How to Add a New Challenge

1. Create a new JSON file in `TTG_Backend/Challenges/`:
    ```json
    {
      "id": 2,
      "name": "Challenge 2: Example",
      "description": "Describe the challenge goal here.",
      "initial_board": [
        [".", ".", ".", ...],  // 17 rows, 15 columns each
        ...
      ],
      "goal": "Describe the win condition."
    }
    ```

2. Reference the challenge by its ID when calling the API.

---

## How to Run the Backend

1. **Install dependencies:**
    ```sh
    pip install fastapi uvicorn openai
    ```

2. **Set your OpenAI API key:**
    ```sh
    export OPENAI_API_KEY=sk-...   # or set in your environment
    ```

3. **Start the FastAPI server:**
    ```sh
    uvicorn app:app --reload
    ```

4. **Test the API:**
    ```sh
    curl -X POST http://localhost:8000/api/solve_challenge -H "Content-Type: application/json" -d '{"challenge_id": "01"}'
    ```

## Docker

To build and run the backend with Docker:

```sh
docker build -t ttg-backend .
docker run -e OPENAI_API_KEY=sk-... -p 8000:8000 ttg-backend
```

You can override the OpenAI API key at runtime using the `-e` flag as shown above.

---

## API Reference

### `POST /api/solve_challenge`

**Request:**
```json
{
  "challenge_id": "01"
}
```

**Response:**
```json
{
  "board": [[...], ...],   // 17x15 solved board
  "metrics": {
    "Simulation Accuracy": "99.9%",
    "State Consistency": "100%",
    "Error Rate": "< 0.1%",
    "Uptime": "99.9%"
  }
}
```

---

## How It Works

- Loads the challenge board and goal from JSON.
- Formats a prompt and sends it to GPT-4V.
- Parses the AI's output for the solved board and metrics.
- Returns the results as JSON for frontend or CLI consumption.

---

## What Was Done in This Project

- Designed a modular backend for Turing Tumble AI challenge solving.
- Implemented challenge loading and management using JSON files.
- Integrated OpenAI GPT-4V for AI-based challenge solving.
- Developed robust parsing for AI output (board and metrics).
- Exposed a clean REST API for frontend or CLI use.
- Documented the backend for easy extension and maintenance.

---

## Contribution

- Add new challenges to `TTG_Backend/Challenges/`.
- Improve board/move/metrics parsing as needed.
- Extend endpoints for more features (e.g., custom prompts, batch solving).

---

## Acknowledgements

- [OpenAI GPT-4V](https://platform.openai.com/docs/guides/vision)
- [Turing Tumble](https://www.turingtumble.com/)

---

## License

[MIT License](LICENSE) 