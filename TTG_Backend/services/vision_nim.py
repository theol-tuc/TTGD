# services/vision_nim.py
import requests
import os
import base64
import json
import uuid
import tempfile
from typing import Dict, Any

def send_to_vila(image_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Send image to NVIDIA VILA API for analysis using the correct API format
    """
    print("=" * 60)
    print("🚀 VILA ANALYSIS STARTED")
    print("=" * 60)
    
    try:
        # Get VILA API credentials from environment variables
        VILA_API_KEY = os.getenv("VILA_API_KEY")
        VILA_API_URL = os.getenv("VILA_API_URL", "https://ai.api.nvidia.com/v1/vlm/nvidia/vila")
        
        print(f"📋 Configuration:")
        print(f"   - API URL: {VILA_API_URL}")
        print(f"   - API Key: {'✅ Configured' if VILA_API_KEY else '❌ Not Found'}")
        
        if not VILA_API_KEY:
            print("⚠️  Warning: VILA_API_KEY not found in environment variables")
            print("   Using fallback analysis...")
            # Return dummy response if no API key
            result = {
                "choices": [
                    {"message": {"content": "add_component(ramp_left, 1, 2)\nadd_component(bit_right, 3, 4)"}}
                ],
                "dummy_analysis": "VILA API key not configured. Please set VILA_API_KEY environment variable."
            }
            print("📤 Fallback Result:", json.dumps(result, indent=2))
            return result
        
        print(f"📁 Processing file: {filename} ({len(image_bytes)} bytes)")
        
        # Save image bytes to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
        
        print(f"💾 Temporary file created: {temp_file_path}")
        
        try:
            # Upload asset to NVCF
            print("📤 Uploading asset to NVCF...")
            asset_id = _upload_asset_to_nvcf(temp_file_path, VILA_API_KEY)
            print(f"✅ Asset uploaded successfully! Asset ID: {asset_id}")
            
            # Prepare the comprehensive query for VILA
            query = (
                "# Template 1 for using library\n"
                "## What is Turing Tumble?\n"
                "Turing Tumble is a mechanical puzzle game that simulates computational logic through the interaction of falling marbles (balls) and configurable parts (blocks) placed on a board.\n"
                "On a game board, falling balls are guided by plug-in building blocks. Individual blocks (bits) can switch between two states (0, 1), thereby changing the path for subsequent balls. Only one ball is in motion at any time. Balls are released from one of two launchers located at the top: blue balls from the left launcher, red balls from the right launcher. \n"
                "Each launcher is controlled by a lever at the bottom edge of the game board. The left lever releases a ball from the left launcher, and the right lever from the right launcher. Initially, one lever is manually activated. The currently configured path then directs the falling ball toward one of the two levers, which automatically triggers the next ball from the corresponding launcher.\n"
                "\n"
                "The game has a predetermined number of marbles to complete challenges and the objective of the game may be to produce a predefined pattern of blue and red balls in the collection trough at the bottom, or to reach specific configurations of blocks that change their position. When the expectedOutput of a challenge is empty, it means to just follow the instruction in the description.\n"
                "\n"
                "Parts:\n"
                "\n"
                "Ball guides:\n"
                "-Ramps (ItemType.RAMP_LEFT or ItemType.RAMP_RIGHT): Direct the ball left or right. These are placed on the board in the initial state to the left and can be flipped.\n"
                "-Crossovers (ItemType.CROSSOVER ): Allow balls coming from the left to go right, and vice versa.\n"
                "\n"
                "Bits (ItemType.BIT_LEFT or ItemType.BIT_RIGHT):\n"
                "-Have two distinct states (flipped to the left or flipped to the right).\n"
                "-Direct balls left or right depending on their current state. A bit flipped to the left will direct the ball to the right, while a bit flipped to the right will direct the ball to the left.\n"
                "-Switches states each time a ball passes through. These are placed on the board in the initial state to the left and can be flipped.\n"
                "\n"
                "Gear bits (ItemType.GEAR_BIT_LEFT or ItemType.GEAR_BIT_RIGHT) and gears (ItemType.GEAR):\n"
                "-Gear bits are similar to bits, but they can be connected by gears and function as a group where every gear bit has the same state.\n"
                "-When a ball passes through a gear bit, the whole group of gear bits switches states.\n"
                "\n"
                "Capture block (ItemType.INTERCEPTOR):\n"
                "-Captures balls and stops the sequence.\n"
                "\n"
                "The function in the library is used to place the named Part on the actual board. The position is a tuple of two integers, representing the x and y coordinates on the board.\n"
                "Empty spaces are where you can place bits, ramps, interceptor, crossover and gear bits.\n"
                "Gray spaces are where you can place gears. The list of functions is later executed by a parser.\n"
                "\n"
                "| Component Type              | Symbol |\n"
                "| --------------------------- | ------ |\n"
                "| `ComponentType.EMPTY`       | `.`    |\n"
                "| `ComponentType.GEAR`        | `G`    |\n"
                "| `ComponentType.BIT_LEFT`    | `L`    |\n"
                "| `ComponentType.BIT_RIGHT`   | `R`    |\n"
                "| `ComponentType.RAMP_LEFT`   | `\\`    |\n"
                "| `ComponentType.RAMP_RIGHT`  | `/`    |\n"
                "| `ComponentType.CROSSOVER`   | `X`    |\n"
                "| `ComponentType.INTERCEPTOR` | `I`    |\n"
                "| `ComponentType.LAUNCHER`    | `S`    |\n"
                "| `ComponentType.LEVER_BLUE`  | `B`    |\n"
                "| `ComponentType.LEVER_RED`   | `r`    |\n"
                "| `ComponentType.GRAY_SPACE`  | `#`    |\n"
                "\n"
                "## Library\n"
                "Solve the challenge using the following function:\n"
                "You are given a 15x17 grid representing a Turing Tumble board. Analyze the following image carefully and return only actual visible components "
                "using this format:\n"
                "\"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)\"\n\n"
                "Do not return more than 15 columns (x: 0-14) or 17 rows (y: 0-16). "
                "Only generate components you clearly see on the board.\n\n"
                "```python\n"
                " def add_component(self, type: ComponentType, x: int, y: int) -> None:\n"
                "    \"\"\"Adds a component of the specified type to the board at position (x, y),\n"
                "    if the position is within the bounds of the board.\"\"\"\n"
                "    if 0 <= x < self.width and 0 <= y < self.height:\n"
                "        self.components[y][x] = Component(type, x, y)\n"
                "```\n"
                "The available component types are defined and named previously ItemType, and the board dimensions are `self.width`(15) × `self.height`(17).\n"
                "\n"
                "## Challenge\n"
                "The challenge you need to solve using the library is: \"id\":  \"1\",\n"
                "board\": board = GameBoard(8,8)\n"
                "board.set_number_of_marbles(8, 8)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 5, 3)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 6, 4)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 7, 5)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 8, 6)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 9, 7)\n"
                "board.add_component(ComponentType.RAMP_RIGHT, 10, 8),\n"
                "red_marbles\": 8,\n"
                "blue_marbles\": 8,\n"
                "description\": \"Make all of the blue marbles (and only the blue marbles) reach the end.\",\n"
                "expectedOutput\": ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'],\n"
                "availableParts\": \"[ItemType.RampLeft]: 4\"\n"
                "\n"
                "## Output\n"
                "The Output should be a single function call that places the next closest and most logical component required to advance the ball's path.\n"
                "The component must be returned using this format:\n"
                "\"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)\"\n"
                "Only return one function call, and make sure it is the **nearest useful move** to where the ball currently is or will be next.\n"
                "Think step-by-step: consider the current ball path and suggest the next component that would help continue the computation correctly.\n"
                "Do not return multiple moves or future steps. Just the immediate next helpful placement.\n"
                "Do not reconstruct the entire board.\n"
                "Ignore arrows or symbols that are not part of official game components.\n"
            )
            print(f"🤖 Query: {query}")
            
            # Call VILA API with the uploaded asset
            print("🔍 Calling VILA API...")
            result = _call_vila_api(VILA_API_URL, VILA_API_KEY, asset_id, query)
            print("✅ VILA API response received!")
            
            # Clean up the asset
            print("🗑️  Cleaning up asset...")
            _delete_asset_from_nvcf(asset_id, VILA_API_KEY)
            print("✅ Asset cleaned up!")
            
            print("📊 VILA Analysis Result:")
            print(json.dumps(result, indent=2))
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                print(f"🗑️  Temporary file cleaned: {temp_file_path}")
        
    except Exception as e:
        print(f"❌ Error in VILA analysis: {e}")
        print(f"📋 Error details: {type(e).__name__}: {str(e)}")
        # Return dummy response on any error
        result = {
            "choices": [
                {"message": {"content": "add_component(ramp_left, 1, 2)\nadd_component(bit_right, 3, 4)"}}
            ],
            "error": f"VILA analysis failed: {str(e)}",
            "dummy_analysis": "Analysis failed, using fallback response."
        }
        print("📤 Error Fallback Result:", json.dumps(result, indent=2))
        return result

def _upload_asset_to_nvcf(media_file: str, api_key: str) -> str:
    """Upload asset to NVCF and return asset ID"""
    print("   📤 Starting asset upload...")
    kNvcfAssetUrl = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    
    # Authorize upload
    print("   🔐 Authorizing upload...")
    authorize = requests.post(
        kNvcfAssetUrl,
        headers=headers,
        json={"contentType": "image/png", "description": "Turing Tumble board analysis"},
        timeout=30,
    )
    authorize.raise_for_status()
    
    authorize_res = authorize.json()
    print(f"   📋 Upload URL received: {authorize_res['uploadUrl'][:50]}...")
    
    # Upload the file
    print("   ⬆️  Uploading file...")
    with open(media_file, "rb") as data_input:
        response = requests.put(
            authorize_res["uploadUrl"],
            data=data_input,
            headers={
                "x-amz-meta-nvcf-asset-description": "Turing Tumble board analysis",
                "content-type": "image/png",
            },
            timeout=300,
        )
    
    response.raise_for_status()
    if response.status_code == 200:
        print(f"   ✅ Upload successful! Asset ID: {authorize_res['assetId']}")
    else:
        print(f"   ❌ Upload failed. Status: {response.status_code}")
    
    return authorize_res["assetId"]

def _call_vila_api(api_url: str, api_key: str, asset_id: str, query: str) -> Dict[str, Any]:
    """Call VILA API with the uploaded asset"""
    print("   🤖 Preparing VILA API call...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_id,
        "NVCF-FUNCTION-ASSET-IDS": asset_id,
        "Accept": "application/json",
    }
    
    media_content = f'<img src="data:image/png;asset_id,{asset_id}" />'
    
    messages = [
        {
            "role": "user",
            "content": f"{query} {media_content}",
        }
    ]
    
    payload = {
        "max_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.7,
        "seed": 50,
        "num_frames_per_inference": 8,
        "messages": messages,
        "stream": False,
        "model": "nvidia/vila",
    }
    
    print("   📡 Sending request to VILA API...")
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    print("   ✅ VILA API response received!")
    print(f"   📊 Response status: {response.status_code}")
    print(f"   📝 Response content preview: {str(result)[:200]}...")
    
    return result

def _delete_asset_from_nvcf(asset_id: str, api_key: str):
    """Delete asset from NVCF"""
    print(f"   🗑️  Deleting asset {asset_id}...")
    kNvcfAssetUrl = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    assert_url = f"{kNvcfAssetUrl}/{asset_id}"
    response = requests.delete(assert_url, headers=headers, timeout=30)
    response.raise_for_status()
    print(f"   ✅ Asset {asset_id} deleted successfully") 