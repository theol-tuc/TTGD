import numpy as np
import re
import random
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM

# ----------------------------
# Connect4 Environment
# ----------------------------
class Connect4Env:
    ROWS, COLS = 6, 7

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1

    def reset(self):
        self.board[:] = 0
        self.current_player = 1
        return self.board.copy()

    def available_actions(self):
        return [c for c in range(self.COLS) if self.board[0][c] == 0]

    def step(self, action):
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][action] == 0:
                self.board[r][action] = self.current_player
                break
        winner = self.check_win(self.current_player)
        done = winner or len(self.available_actions()) == 0
        reward = 1 if winner else 0
        result_player = self.current_player if reward == 1 else 0
        self.current_player = 3 - self.current_player
        return self.board.copy(), reward, done, result_player

    def check_win(self, player):
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.board[r, c+i] == player for i in range(4)):
                    return True
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if all(self.board[r+i, c] == player for i in range(4)):
                    return True
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if all(self.board[r+i, c+i] == player for i in range(4)):
                    return True
        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.board[r-i, c+i] == player for i in range(4)):
                    return True
        return False

# ----------------------------
# Base Agent Classes
# ----------------------------
class BaseAgent:
    def __init__(self, model_id, player_symbol):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_id, pad_token_id=self.tokenizer.pad_token_id).to("cuda")
        self.model.eval()
        self.player_symbol = player_symbol
        self.player_number = 1 if player_symbol == "X" else 2

    def act(self, board):
        board_text = "\n".join(" ".join(['.' if cell == 0 else 'X' if cell == 1 else 'O' for cell in row]) for row in board)
        valid_columns = [str(c) for c in range(7) if board[0][c] == 0]
        prompt = f"""You are a Connect4 AI agent playing as Player {self.player_number} using the symbol '{self.player_symbol}'.
        Your goal is to win the game by connecting four of your symbols ('{self.player_symbol}') in a row: horizontally, vertically, or diagonally before your opponent does.
        The board has 6 rows and 7 columns, and players take turns dropping their symbols into a column.
        Each symbol drops to the lowest empty space in the selected column.
        Valid column indices are from 0 (left) to 6 (right).
        Here is the current board state (top to bottom):
        {board_text}
        Available columns you can drop your piece in: {', '.join(valid_columns)}
        Now, decide carefully and respond with a single digit (0 to 6) for the column number that gives you the best chance to win or blocks your opponent from winning.
        Answer format: only return a single digit (e.g., '3'). No text, explanation, or punctuation."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=3, do_sample=False)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        match = re.search(r'\b[0-6]\b', response)
        return int(match.group()) if match and match.group() in valid_columns else random.choice([int(c) for c in valid_columns])

class LLaMAAgent(BaseAgent):
    def __init__(self, player_symbol):
        super().__init__("meta-llama/Meta-Llama-3-8B-Instruct", player_symbol)

class MistralAgent(BaseAgent):
    def __init__(self, player_symbol):
        super().__init__("mistralai/Mistral-7B-Instruct-v0.3", player_symbol)

class OpenChatAgent(BaseAgent):
    def __init__(self, player_symbol):
        super().__init__("openchat/openchat-3.5-0106", player_symbol)

class MCTSAgent:
    def __init__(self, player_symbol, simulations=5):
        self.player_symbol = player_symbol
        self.player_number = 1 if player_symbol == "X" else 2
        self.simulations = simulations

    def act(self, board):
        action_scores = {a: 0 for a in range(7) if board[0][a] == 0}
        for action in action_scores:
            for _ in range(self.simulations):
                temp_env = Connect4Env()
                temp_env.board = board.copy()
                temp_env.current_player = self.player_number
                _, _, done, winner = temp_env.step(action)
                while not done:
                    valid = temp_env.available_actions()
                    temp_action = random.choice(valid)
                    _, _, done, winner = temp_env.step(temp_action)
                if winner == self.player_number:
                    action_scores[action] += 1
        return max(action_scores, key=action_scores.get)

class LLaMAMCTSAgent:
    def __init__(self, player_symbol, simulations=3):
        self.base_agent = LLaMAAgent(player_symbol)
        self.player_symbol = player_symbol
        self.player_number = 1 if player_symbol == "X" else 2
        self.simulations = simulations

    def act(self, board):
        valid = [c for c in range(7) if board[0][c] == 0]
        results = {}
        for action in valid:
            score = 0
            for _ in range(self.simulations):
                temp_env = Connect4Env()
                temp_env.board = board.copy()
                temp_env.current_player = self.player_number
                _, _, done, winner = temp_env.step(action)
                while not done:
                    if temp_env.current_player == self.player_number:
                        move = self.base_agent.act(temp_env.board)
                    else:
                        move = random.choice(temp_env.available_actions())
                    _, _, done, winner = temp_env.step(move)
                if winner == self.player_number:
                    score += 1
            results[action] = score
        return max(results, key=results.get)

# ----------------------------
# Game runner
# ----------------------------
def play_game(env, agent1, agent2):
    state = env.reset()
    done = False
    agents = {1: agent1, 2: agent2}
    max_turns = 100
    turns = 0
    while not done and turns < max_turns:
        current_player = env.current_player
        action = agents[current_player].act(state)
        if action not in env.available_actions():
            action = random.choice(env.available_actions())
        state, _, done, winner = env.step(action)
        turns += 1
    return winner

# ----------------------------
# Tournament between all agents
# ----------------------------
def run_tournament():
    env = Connect4Env()
    agents = [
        ("LLaMA", LLaMAAgent),
        ("Mistral", MistralAgent),
        ("OpenChat", OpenChatAgent),
        ("MCTS", MCTSAgent),
        ("LLaMA+MCTS", LLaMAMCTSAgent)
    ]
    results = {}

    for i in range(len(agents)):
        for j in range(len(agents)):
            if i == j:
                continue
            name1, Agent1 = agents[i]
            name2, Agent2 = agents[j]
            win1 = win2 = draw = 0
            for game in range(10):
                if game < 5:
                    agent1 = Agent1("X")
                    agent2 = Agent2("O")
                else:
                    agent1 = Agent2("X")
                    agent2 = Agent1("O")
                winner = play_game(env, agent1, agent2)
                if (game < 5 and winner == 1) or (game >= 5 and winner == 2):
                    win1 += 1
                elif (game < 5 and winner == 2) or (game >= 5 and winner == 1):
                    win2 += 1
                else:
                    draw += 1
            results[f"{name1} vs {name2}"] = (win1, win2, draw)

    print("\nConnect4 Tournament Results:")
    for match, res in sorted(results.items()):
        print(f"Match: {match}, {match.split(' vs ')[0]} Wins: {res[0]}, {match.split(' vs ')[1]} Wins: {res[1]}, Draws: {res[2]}")

if __name__ == "__main__":
    run_tournament()

