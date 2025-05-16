import pytest
from TTG_Backend.game_logic import GameBoard, ComponentType, Marble

def test_board_initialization():
    board = GameBoard(8, 8)
    assert board.width == 8
    assert board.height == 8
    assert len(board.components) == 0
    assert len(board.marbles) == 0

def test_add_component():
    board = GameBoard()
    board.add_component(ComponentType.RAMP, 3, 4)
    assert len(board.components) == 1
    assert board.components[0].type == ComponentType.RAMP
    assert board.components[0].position == (3, 4)

def test_remove_component():
    board = GameBoard()
    board.add_component(ComponentType.RAMP, 3, 4)
    board.remove_component(3, 4)
    assert len(board.components) == 0

def test_modify_component():
    board = GameBoard()
    board.add_component(ComponentType.RAMP, 3, 4)
    board.modify_component(3, 4, ComponentType.GEAR)
    assert board.components[0].type == ComponentType.GEAR

def test_add_marble():
    board = GameBoard()
    board.add_marble("blue")
    assert len(board.marbles) == 1
    assert board.marbles[0].color == "blue"
    assert board.marbles[0].active

def test_marble_movement():
    board = GameBoard()
    board.add_component(ComponentType.RAMP, 3, 4)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    
    board.update()
    assert board.marbles[0].position == (4, 5)

def test_interceptor():
    board = GameBoard()
    board.add_component(ComponentType.INTERCEPTOR, 3, 4)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    
    board.update()
    assert not board.marbles[0].active

def test_and_gate():
    board = GameBoard()
    board.add_component(ComponentType.AND_GATE, 3, 4)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    
    # First marble should be stored
    board.update()
    assert board.marbles[0].position == (3, 4)
    
    # Second marble should pass through
    board.add_marble("blue")
    board.marbles[1].position = (3, 4)
    board.update()
    assert board.marbles[1].position == (4, 4)

def test_or_gate():
    board = GameBoard()
    board.add_component(ComponentType.OR_GATE, 3, 4)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    
    board.update()
    assert board.marbles[0].position == (4, 4)

def test_bit():
    board = GameBoard()
    board.add_component(ComponentType.BIT, 3, 4)
    board.add_marble("blue")
    board.marbles[0].position = (3, 4)
    
    board.update()
    assert board.marbles[0].position == (4, 4)
    assert board.components[0].state == 1

def test_board_reset():
    board = GameBoard()
    board.add_component(ComponentType.BIT, 3, 4)
    board.add_marble("blue")
    board.update()
    
    board.reset()
    assert len(board.marbles) == 0
    assert board.components[0].state == 0

def test_invalid_component_position():
    board = GameBoard(8, 8)
    board.add_component(ComponentType.RAMP, 10, 10)  # Invalid position
    assert len(board.components) == 0

def test_multiple_components():
    board = GameBoard()
    board.add_component(ComponentType.RAMP, 3, 4)
    board.add_component(ComponentType.GEAR, 4, 5)
    board.add_component(ComponentType.CROSSOVER, 5, 6)
    
    assert len(board.components) == 3
    assert any(c.type == ComponentType.RAMP for c in board.components)
    assert any(c.type == ComponentType.GEAR for c in board.components)
    assert any(c.type == ComponentType.CROSSOVER for c in board.components) 