import openai
import os
import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict, Any
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from TTG_Backend.board_encoder import BoardEncoder
from TTG_Backend.game_logic import GameBoard, ComponentType
from TTG_Backend.graph_solver import GraphSolver

openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

class TransformerPlanner:
    def __init__(self):
        pass

    def plan(self, prompt: str) -> str:
        """Generate a solution plan using GPT-4 via OpenAI API."""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Turing Tumble puzzle solver."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def parse_plan(self, plan: str) -> list:
        steps = plan.split(". ")
        return [step.strip() for step in steps if step.strip()]

    def get_success_rate(self) -> float:
        """Get the success rate of the planner"""
        return 1.0  # Placeholder - implement actual success tracking
    
    def solve_challenge_with_mcp(self, challenge: Dict[str, Any]) -> Dict[str, Any]:
        """Solve a challenge with Model Context Protocol reporting"""
        # Encode the challenge
        encoded_state = self.encoder.encode_challenge(challenge)
        
        # Generate plan
        plan = self.plan(encoded_state)
        steps = self.parse_plan(plan)
        
        return {
            'plan': plan,
            'steps': steps,
            'success_rate': self.get_success_rate()
        } 