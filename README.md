# Turing Tumble Project

## 📝 Project Update Summary

### 1. Removed LLaVA and Vision Dependencies
- Deleted all code and files related to LLaVA and image-based puzzle solving.
- The project now works **entirely with graph-based puzzle representations** (no image input required).

### 2. New Challenge Solver Script
- Added `solve_all_challenges.py` to automatically load and solve all puzzles from the `Challenges` directory.
- The script uses the AI pipeline (`AIChallengeSolver.py`, `BoardEncoder`, etc.) to generate solutions for each challenge.

### 3. Model File Handling
- **Created a local folder**: `TTG_Backend/models/gpt2` for storing the GPT-2 model and tokenizer files.
- **Important:** The large file `pytorch_model.bin` (over 500MB) is **not tracked by git** due to GitHub's file size limits.
    - Instead, use [Git LFS](https://git-lfs.github.com/) for large files, or download the model manually as described below.

### 4. .gitignore and Git LFS
- Updated `.gitignore` to exclude large binary files (e.g., `*.bin`).
- Configured [Git LFS](https://git-lfs.github.com/) to track large model files if needed.

### 5. Repository Cleanup
- Removed all unnecessary or outdated files.
- Cleaned git history to remove large files that exceeded GitHub's 100MB limit.

### 6. How to Use the Project
- **To run the solver:**  
  ```sh
  python TTG_Backend/solve_all_challenges.py
  ```
- **To set up the model:**  
  - Download the GPT-2 model files from [Hugging Face](https://huggingface.co/gpt2).
  - Place all `.json`, `.txt`, and `pytorch_model.bin` files in `TTG_Backend/models/gpt2/`.
  - If using Git LFS, run:
    ```sh
    git lfs install
    git lfs track "*.bin"
    git add .gitattributes
    git add TTG_Backend/models/gpt2/pytorch_model.bin
    git commit -m "Track large model file with LFS"
    git push origin <your-branch>
    ```

### 7. Branch and Repo Info
- All changes are on the `Rohit` branch of [theol-tuc/TTGD](https://github.com/theol-tuc/TTGD/tree/Rohit).

---

## Note for Collaborators
- **Do not commit large model binaries directly to git.**
- If you clone the repo and the model file is missing, download it manually or use Git LFS.
