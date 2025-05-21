import requests

NIM_API_KEY = "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"  # کلید واقعی‌ات رو بذار اینجا

ASSET_URL = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
INFER_URL = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"

def upload_asset(file: bytes, filename: str, content_type: str):
    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    response = requests.post(
        ASSET_URL,
        headers=headers,
        json={"contentType": content_type, "description": "Uploaded via FastAPI"},
        timeout=300, # 5 minutes timeout for asset creation
    )
    response.raise_for_status()
    upload_url = response.json()["uploadUrl"]
    asset_id = response.json()["assetId"]

    upload_headers = {
        "x-amz-meta-nvcf-asset-description": "Uploaded via FastAPI",
        "content-type": content_type
    }

    upload_response = requests.put(
        upload_url,
        data=file,
        headers=upload_headers,
        timeout=60,
    )
    upload_response.raise_for_status()

    return asset_id

def delete_asset(asset_id: str):
    headers = {"Authorization": f"Bearer {NIM_API_KEY}"}
    requests.delete(f"{ASSET_URL}/{asset_id}", headers=headers)

def send_to_vila(image_bytes: bytes, filename: str):
    ext = filename.split('.')[-1].lower()
    content_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    asset_id = upload_asset(image_bytes, filename, content_type)

    media_tag = f'<img src="data:{content_type};asset_id,{asset_id}" />'
    messages = [{
    "role": "user",
    "content": (
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
        "The challenge you need to solve using the library is: ${question}\n"
        "\n"
        "## Output\n"
        "The Output should be a collection of the functions from the library to be executed in the order they are needed to solve the challenge. The output should be just the newly added parts, and not a reconstruction of the whole board.\n"
        "The output should be a list of function call strings, each using the following format:\n"
        "\"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)\".\n"
        "\n"
        "Output example: [\n"
        "\"add_component(type=ItemType.RAMP_LEFT, x=4, y=0)\",\n"
        "\"add_component(type=ItemType.BIT_LEFT, x=5, y=1)\",\n"
        "\"add_component(type=ItemType.INTERCEPTOR, x=6, y=9)\"\n"
        "]"
    )
}]


    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_id,
        "NVCF-FUNCTION-ASSET-IDS": asset_id,
        "Accept": "application/json"
    }

    payload = {
        "model": "nvidia/vila",
        "messages": messages,
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024,
        "seed": 50
    }

    response = requests.post(INFER_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    delete_asset(asset_id)
    print("VILA API response:", result)

    return result