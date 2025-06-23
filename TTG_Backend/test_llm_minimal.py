import requests

def test_minimal_prompt():
    prompt = """[
  "add_component(type=ItemType.RampLeft, x=4, y=2)",
  "add_component(type=ItemType.RampLeft, x=6, y=4)"
]"""

    print("🔵 Sending minimal prompt to LLaMA server...")
    print(f"Prompt: {repr(prompt)}")
    
    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json={"prompt": prompt, "max_tokens": 100, "temperature": 0.2}
        )
        
        print(f"\n🔵 Response status: {response.status_code}")
        print(f"🔵 Raw response text: {repr(response.text)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔵 Parsed response: {result}")
            
            output = result.get('output', '')
            print(f"🔵 LLM output: {repr(output)}")
            
            if output.strip():
                print("✅ LLM produced output!")
            else:
                print("❌ LLM returned empty output")
        else:
            print(f"❌ Server error: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to LLaMA server!")
        print("Make sure SSH tunnel is active and server is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_with_higher_temperature():
    prompt = """[
  "add_component(type=ItemType.RampLeft, x=4, y=2)",
  "add_component(type=ItemType.RampLeft, x=6, y=4)"
]"""

    print("\n🔥 Testing with higher temperature (0.7)...")
    
    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json={"prompt": prompt, "max_tokens": 100, "temperature": 0.7}
        )
        
        if response.status_code == 200:
            result = response.json()
            output = result.get('output', '')
            print(f"🔥 LLM output with temp=0.7: {repr(output)}")
            
            if output.strip():
                print("✅ Higher temperature worked!")
            else:
                print("❌ Still empty even with higher temperature")
        else:
            print(f"❌ Server error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_minimal_prompt()
    test_with_higher_temperature() 