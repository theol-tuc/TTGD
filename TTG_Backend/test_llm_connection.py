import requests
import json
import sys
from datetime import datetime

def test_llm_connection():
    """Test the connection to the LLM server and verify response format."""
    print("\n=== Testing LLM Server Connection ===\n")
    
    # Test URL
    url = "http://localhost:8001/generate"
    
    # Simple test prompt
    test_prompt = """
You are playing a marble game. The current state is:
{
    "components": [],
    "marbles": [],
    "red_marbles": 3,
    "blue_marbles": 3,
    "active_launcher": "left"
}

Please provide your next move in JSON format.
"""
    
    print("Sending test request to LLM server...")
    print(f"URL: {url}")
    print("\nTest Prompt:")
    print(test_prompt)
    
    try:
        # Send request
        response = requests.post(
            url,
            json={"prompt": test_prompt},
            timeout=30
        )
        
        # Check response
        if response.status_code == 200:
            print("\n✅ Successfully connected to LLM server!")
            
            # Parse and validate response
            result = response.json()
            if "response" in result:
                print("\nResponse received:")
                print(json.dumps(result["response"], indent=2))
                
                # Validate response format
                required_fields = ["action", "parameters", "explanation"]
                missing_fields = [field for field in required_fields if field not in result["response"]]
                
                if missing_fields:
                    print(f"\n❌ Response missing required fields: {missing_fields}")
                else:
                    print("\n✅ Response format is valid!")
            else:
                print("\n❌ Response missing 'response' field")
                print("Raw response:", result)
        else:
            print(f"\n❌ Server returned error: {response.status_code}")
            print("Error details:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to LLM server!")
        print("\nMake sure you have an active SSH tunnel with:")
        print("ssh -L 8001:localhost:8001 mtko19@cloud-247.rz.tu-clausthal.de")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_llm_connection() 