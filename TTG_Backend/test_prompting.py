from prompting import prompt_manager

def test_prompt():
    # Create a test game state
    game_state = {
        "components": [
            {"type": "gear", "x": 3, "y": 3, "rotation": 0},
            {"type": "ramp", "x": 4, "y": 4, "rotation": 90}
        ],
        "marbles": [
            {"color": "red", "x": 0, "y": 0},
            {"color": "blue", "x": 1, "y": 1}
        ],
        "red_marbles": 3,
        "blue_marbles": 3,
        "active_launcher": "left"
    }

    # Test with a challenge
    challenge_id = "challenge_1"
    
    # Generate prompt
    prompt = prompt_manager.generate_prompt('library', game_state, challenge_id)
    
    print("\n🧪 Rendered Prompt:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
    
    # Validate prompt structure
    assert "<s>[INST]" in prompt, "Missing LLaMA 3 start token"
    assert "[/INST]" in prompt, "Missing LLaMA 3 end token"
    assert "<<SYSTEM>>" in prompt, "Missing system prompt"
    assert "Current Game State" in prompt, "Missing game state"
    assert "JSON format" in prompt, "Missing JSON format instructions"
    
    print("\n✅ Prompt validation passed!")

if __name__ == "__main__":
    test_prompt() 