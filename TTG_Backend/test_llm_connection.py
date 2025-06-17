import requests

def test_llama_server():
    prompt = """
You are a JSON generator.

Return only:
[
  "add_component(type=ItemType.RAMP_LEFT, x=4, y=0)"
]
No explanations.

Current Game State:
{ "components": [], "marbles": [], "red_marbles": 3, "blue_marbles": 3, "active_launcher": "left" }
"""

    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json={
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.3
            }
        )
        
        if response.status_code == 200:
            print("\n✅ Successfully connected to LLaMA server!")
            print("\nResponse:")
            print(response.json())
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