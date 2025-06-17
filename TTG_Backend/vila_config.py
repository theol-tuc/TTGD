# VILA Configuration Helper
import os
from dotenv import load_dotenv

def setup_vila_config():
    """
    Setup VILA API configuration
    """
    load_dotenv()
    
    # Check if VILA API key is set
    vila_api_key = os.getenv("VILA_API_KEY")
    vila_api_url = os.getenv("https://ai.api.nvidia.com/v1/vlm/nvidia/vila")
    
    if not vila_api_key:
        print("⚠️  VILA_API_KEY not found in environment variables")
        print("To use real VILA analysis, please:")
        print("1. Get your VILA API key from NVIDIA")
        print("2. Create a .env file in the TTG_Backend directory")
        print("3. Add: VILA_API_KEY=your_api_key_here")
        print("4. Add: VILA_API_URL=your_vila_endpoint_url")
        return False
    
    if not vila_api_url:
        print("⚠️  VILA_API_URL not found in environment variables")
        print("Please add VILA_API_URL to your .env file")
        return False
    
    print("✅ VILA API configuration found")
    print(f"API URL: {vila_api_url}")
    print("API Key: [CONFIGURED]")
    return True

if __name__ == "__main__":
    setup_vila_config() 