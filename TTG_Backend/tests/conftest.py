import pytest
from TTG_Backend.game_logic import GameBoard, ComponentType, Marble

@pytest.fixture
def empty_board():
    return GameBoard(8, 8)

@pytest.fixture
def board_with_components():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.RAMP, 3, 4)
    board.add_component(ComponentType.GEAR, 4, 5)
    board.add_component(ComponentType.CROSSOVER, 5, 6)
    return board

@pytest.fixture
def board_with_marble():
    board = GameBoard(8, 8)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    return board 