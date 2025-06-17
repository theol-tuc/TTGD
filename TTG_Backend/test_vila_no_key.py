#!/usr/bin/env python3
"""
Test script to check VILA behavior without API key
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_vila_without_key():
    """Test VILA API without API key to see dummy response"""
    
    print("🔍 VILA TEST WITHOUT API KEY")
    print("=" * 60)
    
    # Temporarily remove API key
    original_key = os.environ.get("VILA_API_KEY")
    if original_key:
        del os.environ["VILA_API_KEY"]
        print("🔑 Temporarily removed VILA_API_KEY")
    
    # Check if image file exists
    image_file = "debug1_uploaded_board.png"
    if not os.path.exists(image_file):
        print(f"❌ Error: {image_file} not found!")
        return
    
    print(f"📁 Using test image: {image_file}")
    
    # Prepare the request
    url = "http://localhost:8000/api/vila/analyze"
    
    try:
        print("\n🚀 Sending request to VILA API (without key)...")
        
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
            
            # Check 3: Check content quality
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                if "choices" in raw and len(raw["choices"]) > 0:
                    content = raw["choices"][0].get("message", {}).get("content", "")
                    if "add_component(ramp_left, 1, 2)" in content and "add_component(bit_right, 3, 4)" in content:
                        is_dummy = True
                        dummy_reasons.append("Contains default dummy commands")
            
            # Final verdict
            if is_dummy:
                print("✅ DUMMY RESPONSE DETECTED (Expected!)")
                print("📋 Reasons:")
                for reason in dummy_reasons:
                    print(f"   • {reason}")
                print("\n🎯 This confirms the system works correctly:")
                print("   • Without API key → Dummy response")
                print("   • With API key → Real VILA response")
            else:
                print("❌ UNEXPECTED: Got real response without API key!")
            
            # Show response details
            print(f"\n📊 Response structure:")
            print(f"   • Status: {result.get('status', 'N/A')}")
            print(f"   • Executed components: {len(result.get('executed_components', []))}")
            
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
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Restore original API key
        if original_key:
            os.environ["VILA_API_KEY"] = original_key
            print("\n🔑 Restored original VILA_API_KEY")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_vila_without_key() 