#!/usr/bin/env python3
"""
Test script to detect if VILA API returns real responses or dummy responses
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_vila_detection():
    """Test VILA API and detect if response is real or dummy"""
    
    print("🔍 VILA RESPONSE DETECTION TEST")
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
        print("💡 This means you'll get DUMMY responses")
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
            
            print("\n🔍 RESPONSE ANALYSIS:")
            print("-" * 40)
            
            # Check for dummy indicators
            is_dummy = False
            dummy_reasons = []
            
            # Check 1: Look for dummy_analysis field
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                if "dummy_analysis" in raw:
                    is_dummy = True
                    dummy_reasons.append(f"dummy_analysis field found: {raw['dummy_analysis']}")
            
            # Check 2: Look for error field
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                if "error" in raw:
                    is_dummy = True
                    dummy_reasons.append(f"error field found: {raw['error']}")
            
            # Check 3: Check if response has choices structure
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                if "choices" not in raw:
                    is_dummy = True
                    dummy_reasons.append("No 'choices' field in response")
            
            # Check 4: Check content quality
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                if "choices" in raw and len(raw["choices"]) > 0:
                    content = raw["choices"][0].get("message", {}).get("content", "")
                    if not content or len(content) < 10:
                        is_dummy = True
                        dummy_reasons.append("Content too short or empty")
                    elif "add_component(ramp_left, 1, 2)" in content and "add_component(bit_right, 3, 4)" in content:
                        is_dummy = True
                        dummy_reasons.append("Contains default dummy commands")
            
            # Check 5: Check executed components
            if "executed_components" in result:
                components = result["executed_components"]
                if len(components) == 0:
                    is_dummy = True
                    dummy_reasons.append("No executed components")
                elif len(components) == 2 and "ramp_left" in str(components) and "bit_right" in str(components):
                    is_dummy = True
                    dummy_reasons.append("Default dummy components detected")
            
            # Final verdict
            if is_dummy:
                print("❌ DUMMY RESPONSE DETECTED!")
                print("📋 Reasons:")
                for reason in dummy_reasons:
                    print(f"   • {reason}")
                print("\n💡 To get real VILA responses:")
                print("   1. Make sure VILA_API_KEY is set correctly")
                print("   2. Check your internet connection")
                print("   3. Verify the VILA API is accessible")
            else:
                print("✅ REAL VILA RESPONSE DETECTED!")
                print("🎉 You're getting actual AI analysis from NVIDIA VILA!")
            
            # Show response details
            print(f"\n📊 Response structure:")
            print(f"   • Status: {result.get('status', 'N/A')}")
            print(f"   • Executed components: {len(result.get('executed_components', []))}")
            print(f"   • Confidence: {result.get('confidence', 'N/A')}")
            
            if "raw_response" in result:
                raw = result["raw_response"]
                print(f"   • Raw response type: {type(raw)}")
                if isinstance(raw, dict):
                    print(f"   • Raw response keys: {list(raw.keys())}")
                    if "choices" in raw and len(raw["choices"]) > 0:
                        content = raw["choices"][0].get("message", {}).get("content", "")
                        print(f"   • Content preview: {content[:100]}...")
            
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on port 8000")
        print("💡 Run: python run.py")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_vila_detection() 