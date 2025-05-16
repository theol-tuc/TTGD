"""
Turing Tumble AI Challenge Solver
A package for solving Turing Tumble challenges using AI techniques.
"""

from .solver import solve_challenge
from .challenges import CHALLENGES
from .graph_parser import GraphVizParser
from .graph_solver import GraphNeuralNetwork
# from .llava_solver import LLaVASolver  # Removed, file deleted

__version__ = "0.1.0"
__all__ = [
    'solve_challenge',
    'CHALLENGES',
    'GraphVizParser',
    'GraphNeuralNetwork'
    # 'LLaVASolver'  # Removed
] 