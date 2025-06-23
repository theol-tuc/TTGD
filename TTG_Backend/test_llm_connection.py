import requests
import re
import json

def extract_json_from_response(response_text):
    """
    Extract JSON array from the model response, removing any explanatory text.
    """
    # Try to find JSON array pattern
    json_match = re.search(r"\[\s*\"add_component.*?\]", response_text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # Safety net: find the last complete JSON array
    end_index = response_text.rfind("]")
    if end_index != -1:
        start_index = response_text.rfind("[", 0, end_index + 1)
        if start_index != -1:
            return response_text[start_index:end_index + 1]
    
    # If no match found, return the original response
    return response_text

def test_llama_server():
    prompt = """Only return a JSON list of at most 4 add_component function calls.
Do NOT write any explanations, comments, functions, or extra output.
The format must be:

[
  "add_component(type=ItemType.RampLeft, x=6, y=6)",
  "add_component(type=ItemType.RampLeft, x=8, y=6)"
]

Your response must start with [ and end with ].
If you return anything else, it will crash the game.

Game State:
{
  "components": [],
  "marbles": [],
  "red_marbles": 3,
  "blue_marbles": 3,
  "active_launcher": "left"
}

Remember: ONLY return the JSON list with at most 4 components. Nothing else."""

    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json={
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.4
            }
        )
        
        if response.status_code == 200:
            print("\n✅ Successfully connected to LLaMA server!")
            print("\nRaw Response:")
            print(response.json())
            
            # Extract clean JSON
            raw_output = response.json().get('output', '')
            clean_json = extract_json_from_response(raw_output)
            
            print("\n🧹 Cleaned JSON:")
            print(clean_json)
            
            # Check for empty response
            if not raw_output.strip():
                print("\n⚠️ WARNING: LLM returned empty response!")
                print(f"Raw output: {repr(raw_output)}")
                return
            
            # Try to parse as JSON to validate
            try:
                parsed = json.loads(clean_json)
                print("\n✅ Valid JSON parsed successfully!")
                print(f"Number of components suggested: {len(parsed)}")
                
                # Show the components
                for i, component in enumerate(parsed):
                    print(f"  Component {i+1}: {component}")
                    
            except json.JSONDecodeError as e:
                print(f"\n⚠️ JSON parsing failed: {e}")
                print(f"Attempted to parse: {repr(clean_json)}")
                
        else:
            print(f"\n❌ Server returned error: {response.status_code}")
            print("Error details:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to LLaMA server!")
        print("\nMake sure you have an active SSH tunnel with:")
        print("ssh -L 8001:localhost:8001 mtko19@cloud-247.rz.tu-clausthal.de")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_llama_server() 