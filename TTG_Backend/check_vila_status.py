#!/usr/bin/env python3
"""
Comprehensive VILA Status Checker
"""

import os
import requests
import json
from dotenv import load_dotenv

def check_vila_status():
    """Complete VILA status check"""
    
    print("🔍 Comprehensive VILA Status Check")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    api_key = os.getenv("VILA_API_KEY")
    api_url = os.getenv("VILA_API_URL", "https://ai.api.nvidia.com/v1/vlm/nvidia/vila")
    
    print("📋 Configuration Status:")
    print(f"   🔑 API Key: {'✅ Configured' if api_key else '❌ Not Configured'}")
    print(f"   🌐 API URL: {api_url}")
    
    if not api_key:
        print("\n⚠️  Warning: API Key not configured!")
        print("💡 To get real VILA responses:")
        print("   1. Create .env file in TTG_Backend folder")
        print("   2. Add VILA_API_KEY=your_api_key_here")
        print("   3. Restart the server")
    
    # Check if image file exists
    image_file = "debug1_uploaded_board.png"
    if not os.path.exists(image_file):
        print(f"\n❌ Error: File {image_file} not found!")
        return
    
    print(f"\n📁 Test file: {image_file}")
    print(f"📊 File size: {os.path.getsize(image_file)} bytes")
    
    # Test API endpoint
    url = "http://localhost:8000/api/vila/analyze"
    
    try:
        print("\n🚀 Sending request to VILA API...")
        
        with open(image_file, "rb") as f:
            files = {"board_image": (image_file, f, "image/png")}
            response = requests.post(url, files=files, timeout=120)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n🔍 Response Analysis:")
            print("-" * 40)
            
            # Determine response type
            is_real = True
            reasons = []
            
            # Check for real response indicators
            if "raw_response" in result and isinstance(result["raw_response"], dict):
                raw = result["raw_response"]
                
                # Check for dummy indicators
                if "dummy_analysis" in raw:
                    is_real = False
                    reasons.append("dummy_analysis field found")
                
                if "error" in raw:
                    is_real = False
                    reasons.append("error field found")
                
                # Check for real response indicators
                if "id" in raw and "model" in raw and "choices" in raw:
                    if raw.get("model") == "nvidia/vila":
                        reasons.append("Response from nvidia/vila model")
                    else:
                        is_real = False
                        reasons.append(f"Unknown model: {raw.get('model')}")
                else:
                    is_real = False
                    reasons.append("Incomplete response structure")
                
                # Check content quality
                if "choices" in raw and len(raw["choices"]) > 0:
                    content = raw["choices"][0].get("message", {}).get("content", "")
                    if "add_component(ramp_left, 1, 2)" in content and "add_component(bit_right, 3, 4)" in content:
                        is_real = False
                        reasons.append("Dummy commands found")
                    elif len(content) > 50:
                        reasons.append("Response content is long and diverse")
            
            # Final verdict
            if is_real:
                print("✅ Real VILA response detected!")
                print("🎉 You are receiving real analysis from NVIDIA VILA!")
            else:
                print("❌ Dummy response detected!")
                print("📋 Reasons:")
                for reason in reasons:
                    print(f"   • {reason}")
            
            # Show response details
            print(f"\n📊 Response Details:")
            print(f"   • Status: {result.get('status', 'N/A')}")
            print(f"   • Executed components count: {len(result.get('executed_components', []))}")
            print(f"   • Confidence: {result.get('confidence', 'N/A')}")
            
            if "raw_response" in result:
                raw = result["raw_response"]
                print(f"   • Raw response type: {type(raw)}")
                if isinstance(raw, dict):
                    print(f"   • Raw response keys: {list(raw.keys())}")
                    if "choices" in raw and len(raw["choices"]) > 0:
                        content = raw["choices"][0].get("message", {}).get("content", "")
                        print(f"   • Content preview: {content[:100]}...")
            
            # Show executed components
            if "executed_components" in result:
                components = result["executed_components"]
                print(f"\n🎮 Executed components ({len(components)}):")
                for i, comp in enumerate(components[:5], 1):  # Show first 5
                    print(f"   {i}. {comp}")
                if len(components) > 5:
                    print(f"   ... and {len(components) - 5} more components")
            
        else:
            print(f"❌ Request failed with error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure FastAPI server is running on port 8000")
        print("💡 To start server: python run.py")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
    print("📚 For more information, read VILA_DETECTION_GUIDE.md")

if __name__ == "__main__":
    check_vila_status() 