#!/usr/bin/env python3
"""
Test script to check if VILA API returns real responses or demo responses
"""

import os
os.environ['VILA_API_KEY'] = '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'
os.environ['VILA_API_URL'] = 'https://ai.api.nvidia.com/v1/vlm/nvidia/vila'

from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_vila_api():
    """Test VILA API with a real image file"""
    
    print("🧪 TESTING VILA API - REAL vs DEMO RESPONSE")
    print("=" * 60)
    
    # Check if image file exists
    image_file = "debug1_uploaded_board.png"
    if not os.path.exists(image_file):
        print(f"❌ Error: {image_file} not found!")
        return
    
    print(f"📁 Using test image: {image_file}")
    print(f"📊 File size: {os.path.getsize(image_file)} bytes")
    
    # Check environment variables
    api_key = os.getenv("VILA_API_KEY")
    api_url = os.getenv("VILA_API_URL")
    
    print(f"🔑 API Key: {'✅ Configured' if api_key else '❌ Not Found'}")
    print(f"🌐 API URL: {api_url}")
    
    if not api_key:
        print("❌ VILA_API_KEY not found in environment variables!")
        return
    
    # Prepare the request
    url = "http://localhost:8000/api/vila/analyze"
    
    try:
        print("\n🚀 Sending request to VILA API...")
        
        with open(image_file, "rb") as f:
            files = {"board_image": (image_file, f, "image/png")}
            response = requests.post(url, files=files, timeout=120)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n📋 RESPONSE ANALYSIS:")
            print("-" * 40)
            
            # Check if it's a real response or demo
            if "dummy_analysis" in result:
                print("❌ DEMO RESPONSE DETECTED!")
                print(f"   Reason: {result['dummy_analysis']}")
            elif "error" in result:
                print("❌ ERROR RESPONSE DETECTED!")
                print(f"   Error: {result['error']}")
            else:
                print("✅ REAL VILA RESPONSE DETECTED!")
            
            # Show response details
            print(f"\n📊 Response keys: {list(result.keys())}")
            
            if "raw_response" in result:
                raw = result["raw_response"]
                print(f"📝 Raw response type: {type(raw)}")
                if isinstance(raw, dict) and "choices" in raw:
                    content = raw["choices"][0]["message"]["content"]
                    print(f"🤖 VILA Analysis: {content[:200]}...")
            
            if "executed_components" in result:
                components = result["executed_components"]
                print(f"🎮 Executed components: {len(components)}")
                for i, comp in enumerate(components, 1):
                    print(f"   {i}. {comp}")
            
            if "recommended_move" in result:
                print(f"🎯 Recommended move: {result['recommended_move']}")
            
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_vila_api() 