# Project Structure and Backend Implementation Guide

This document explains the structure of the Turing Tumble AI Solver backend, the purpose of each main file and folder, and what was implemented in this project.

---

## Directory Overview

```
TTG_Backend/
├── app.py                # FastAPI app with API endpoints
├── ttg_demo.py           # Script for local testing/demo
├── Challenges/
│   ├── challenge_01.json # Example challenge file
│   └── ...               # More challenge files
├── game_logic.py         # (If used) Board logic and simulation
├── game_state.py         # (If used) Board state serialization/deserialization
├── Docs/
│   └── PROJECT_STRUCTURE.md # This documentation file
└── ...                   # Other backend files
```

---

## File and Folder Explanations

### `app.py`
- **Purpose:** Main FastAPI application. Exposes REST API endpoints, including `/api/solve_challenge`.
- **Key Logic:**
  - Loads challenge data from JSON files.
  - Formats prompts for GPT-4V.
  - Calls the OpenAI API to solve challenges.
  - Parses the AI's output for the solved board and metrics.
  - Returns results as JSON for frontend or CLI use.

### `ttg_demo.py`
- **Purpose:** Standalone script for local testing and demonstration.
- **Key Logic:**
  - Can load a challenge, call GPT-4V, and print the solution and metrics in the console.

### `Challenges/`
- **Purpose:** Stores all challenge definitions as JSON files.
- **File Format:**
  - Each file (e.g., `challenge_01.json`) contains:
    - `id`: Challenge number
    - `name`: Challenge name
    - `description`: Challenge description
    - `initial_board`: 17x15 board matrix
    - `goal`: Text description of the win condition

### `game_logic.py` (if present)
- **Purpose:** Contains board logic, simulation, or helper functions for board manipulation.

### `game_state.py` (if present)
- **Purpose:** Handles serialization/deserialization of the board state, possibly for saving/loading or API responses.

### `Docs/`
- **Purpose:** Contains documentation files to help developers and reviewers understand the project.
- **Key File:**
  - `PROJECT_STRUCTURE.md`: This file, explaining the codebase and your contributions.

---

## What Was Implemented in the Backend

- **Challenge Management:**
  - Challenges are defined as JSON files for easy addition and management.
- **AI Integration:**
  - The backend formats the board and goal as a prompt and sends it to GPT-4V.
  - The AI's output is parsed for a solved board (17x15) and performance metrics.
- **REST API:**
  - `/api/solve_challenge` endpoint accepts a challenge ID and returns the solution and metrics as JSON.
- **Parsing Utilities:**
  - Functions to robustly extract the board matrix and metrics from GPT-4V's output.
- **Documentation:**
  - Comprehensive README and this project structure guide for maintainability and onboarding.

---

## How to Extend or Maintain

- **Add new challenges:** Place new JSON files in `Challenges/`.
- **Update AI logic:** Modify prompt formatting or parsing as needed in `app.py`.
- **Add endpoints:** Extend `app.py` for new features (e.g., batch solving, custom prompts).
- **Improve documentation:** Add more files to `Docs/` as the project grows.

---

## Summary

This backend is designed for clarity, modularity, and easy extension. All major logic is documented and separated by responsibility, making it straightforward for new developers or reviewers to understand and contribute. 