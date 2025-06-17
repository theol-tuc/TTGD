import requests
import os

# Set environment variables directly
os.environ['VILA_API_KEY'] = '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'
os.environ['VILA_API_URL'] = 'https://ai.api.nvidia.com/v1/vlm/nvidia/vila'

def test_vila_endpoint():
    print("🧪 Testing VILA endpoint...")
    
    # Check if image file exists
    image_file = "debug1_uploaded_board.png"
    if not os.path.exists(image_file):
        print(f"❌ Error: {image_file} not found!")
        return
    
    print(f"📁 Using test image: {image_file}")
    
    # Send request
    url = "http://localhost:8000/api/vila/analyze"
    
    try:
        print("🚀 Sending request...")
        with open(image_file, "rb") as f:
            files = {"board_image": (image_file, f, "image/png")}
            response = requests.post(url, files=files, timeout=120)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📊 Response keys: {list(result.keys())}")
            
            if "executed_components" in result:
                components = result["executed_components"]
                print(f"🎮 Executed components: {len(components)}")
                for i, comp in enumerate(components, 1):
                    print(f"   {i}. {comp}")
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_vila_endpoint() 