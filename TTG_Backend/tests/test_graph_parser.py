import pytest
import os
from ..graph_parser import GraphVizParser
from ..game_logic import GameBoard, ComponentType

@pytest.fixture
def parser():
    return GraphVizParser()

@pytest.fixture
def test_challenge_dir(tmp_path):
    # Create a temporary directory with test challenge files
    challenge_dir = tmp_path / "Challenges"
    challenge_dir.mkdir()
    
    # Create a test challenge file
    challenge_file = challenge_dir / "puzzle01-1.gv"
    challenge_file.write_text("""
    digraph Challenge01 {
        graph [ GRAPH_STYLE ]
        node  [ NODE_STYLE  ]
        edge  [ EDGE_STYLE  ]
        
        RAMP_5_3 [label="RAMP_5_3"]
        RAMP_5_5 [label="RAMP_5_5"]
        GEAR_4_4 [label="GEAR_4_4"]
        
        RAMP_5_3 -> GEAR_4_4
        GEAR_4_4 -> RAMP_5_5
    }
    """)
    
    return challenge_dir

def test_get_challenge_file(parser, test_challenge_dir):
    parser.challenges_dir = str(test_challenge_dir)
    file_path = parser.get_challenge_file("01")
    assert os.path.exists(file_path)
    assert "puzzle01-1.gv" in file_path

def test_parse_gv_file(parser, test_challenge_dir):
    parser.challenges_dir = str(test_challenge_dir)
    file_path = parser.get_challenge_file("01")
    graph_data = parser.parse_gv_file(file_path, "01")
    
    assert 'nodes' in graph_data
    assert 'edges' in graph_data
    assert len(graph_data['nodes']) == 3
    assert len(graph_data['edges']) == 2

def test_convert_to_board(parser, test_challenge_dir):
    parser.challenges_dir = str(test_challenge_dir)
    file_path = parser.get_challenge_file("01")
    graph_data = parser.parse_gv_file(file_path, "01")
    board = parser.convert_to_board(graph_data)
    
    assert isinstance(board, GameBoard)
    assert len(board.components) > 0

def test_visualize_challenge(parser, test_challenge_dir, tmp_path):
    parser.challenges_dir = str(test_challenge_dir)
    save_path = tmp_path / "test_visualization.png"
    success = parser.visualize_challenge("01", str(save_path))
    
    assert success
    assert save_path.exists()

def test_export_challenge_json(parser, test_challenge_dir, tmp_path):
    parser.challenges_dir = str(test_challenge_dir)
    save_path = tmp_path / "test_challenge.json"
    success = parser.export_challenge_json("01", str(save_path))
    
    assert success
    assert save_path.exists()
    
    # Verify JSON content
    import json
    with open(save_path) as f:
        data = json.load(f)
        assert 'id' in data
        assert 'nodes' in data
        assert 'edges' in data
        assert 'board_state' in data

def test_create_challenge_variation(parser, test_challenge_dir):
    parser.challenges_dir = str(test_challenge_dir)
    success = parser.create_challenge_variation(
        "01",
        "1",
        [{
            'type': 'add_component',
            'component_type': 'RAMP',
            'x': 5,
            'y': 5
        }]
    )
    
    assert success
    variation_path = os.path.join(
        test_challenge_dir,
        "puzzle01-var1.gv"
    )
    assert os.path.exists(variation_path)

def test_invalid_challenge_id(parser):
    with pytest.raises(FileNotFoundError):
        parser.get_challenge_file("99")

def test_invalid_component_type(parser, test_challenge_dir):
    parser.challenges_dir = str(test_challenge_dir)
    with pytest.raises(KeyError):
        parser.create_challenge_variation(
            "01",
            "1",
            [{
                'type': 'add_component',
                'component_type': 'INVALID',
                'x': 5,
                'y': 5
            }]
        ) 