# Turing Tumble Project

## 📝 Project Update Summary

### 1. Removed LLaVA and Vision Dependencies
- Deleted all code and files related to LLaVA and image-based puzzle solving.
- The project now works **entirely with graph-based puzzle representations** (no image input required).

### 2. New Challenge Solver Script
- Added `solve_all_challenges.py` to automatically load and solve all puzzles from the `Challenges` directory.
- The script uses the AI pipeline (`AIChallengeSolver.py`, `BoardEncoder`, etc.) to generate solutions for each challenge **using GPT-4V via API**.

### 3. Model File Handling
- **No local model files are required.**
- The project uses **OpenAI's GPT-4V model via API** for all AI and puzzle-solving tasks.
- You only need to set up your OpenAI API key in the environment or configuration as described below.

### 4. .gitignore and Git LFS
- Updated `.gitignore` to exclude large binary files (e.g., `*.bin`).
- **No need for Git LFS or local model binaries.**

### 5. Repository Cleanup
- Removed all unnecessary or outdated files.
- Cleaned git history to remove large files that exceeded GitHub's 100MB limit.

### 6. How to Use the Project
- **To run the solver:**  
  ```sh
  python TTG_Backend/solve_all_challenges.py
  ```
- **To set up the API key:**  
  - Obtain an OpenAI API key with access to GPT-4V.
  - Set the API key as an environment variable or in the project configuration (see `TTG_Backend/config.py`).

### 7. Branch and Repo Info
- All changes are on the `Rohit` branch of [theol-tuc/TTGD](https://github.com/theol-tuc/TTGD/tree/Rohit).

---

## Note for Collaborators
- **Do not commit any API keys or sensitive credentials to git.**
- If you clone the repo, make sure to set up your own OpenAI API key for GPT-4V access.
