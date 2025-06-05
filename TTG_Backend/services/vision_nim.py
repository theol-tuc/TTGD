import requests
from datasets import load_dataset, DatasetDict
from transformers import AutoProcessor
from PIL import Image
import os

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
        "You are given a 15x17 grid representing a Turing Tumble board. Analyze the following image carefully and return only actual visible components "
        "using this format:\n"
        "\"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)\"\n\n"
        "Do not return more than 15 columns (x: 0-14) or 17 rows (y: 0-16). "
        "Only generate components you clearly see on the board.\n\n"
        f"{media_tag}"
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
        "The Output should be a single function call that places the next closest and most logical component required to advance the ball’s path.\n"
        "The component must be returned using this format:\n"
        "\"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)\"\n"
        "Only return one function call, and make sure it is the **nearest useful move** to where the ball currently is or will be next.\n"
        "Think step-by-step: consider the current ball path and suggest the next component that would help continue the computation correctly.\n"
        "Do not return multiple moves or future steps. Just the immediate next helpful placement.\n"
        "Do not reconstruct the entire board.\n"
        "Ignore arrows or symbols that are not part of official game components.\n"


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
        "temperature": 0.3,
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

# Import necessary libraries
# from datasets import load_dataset, DatasetDict
# from transformers import AutoProcessor
# from PIL import Image
# import os

# Step 1: Load the dataset
# Assuming the dataset is stored in a folder with images and a JSONL file
def load_turing_tumble_dataset(dataset_path: str) -> DatasetDict:
    """
    Loads the Turing Tumble dataset from a folder containing images and a JSONL file.

    Args:
        dataset_path (str): Path to the dataset folder.

    Returns:
        DatasetDict: A Hugging Face DatasetDict object containing the dataset.
    """
    # Load the JSONL file as a Hugging Face dataset
    dataset = load_dataset("json", data_files=os.path.join(dataset_path, "data.jsonl"))

    # Add the image paths to the dataset
    def add_image_path(example):
        example["image"] = os.path.join(dataset_path, example["image_file"])
        return example

    dataset = dataset.map(add_image_path)
    return dataset

# Step 2: Preprocess the dataset
def preprocess_dataset(dataset: DatasetDict, processor: AutoProcessor) -> DatasetDict:
    """
    Preprocesses the dataset by tokenizing the instructions and processing the images.

    Args:
        dataset (DatasetDict): The dataset to preprocess.
        processor (AutoProcessor): The processor for the VILA model.

    Returns:
        DatasetDict: The preprocessed dataset.
    """
    def preprocess(example):
        # Load the image
        image = Image.open(example["image"]).convert("RGB")

        # Tokenize the instruction and process the image
        inputs = processor(
            text=example["instruction"],
            images=image,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )

        # Add the expected output as labels
        inputs["labels"] = processor.tokenizer(
            example["expected_output"],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=128
        )["input_ids"]

        return {
            "pixel_values": inputs["pixel_values"].squeeze(0),
            "input_ids": inputs["input_ids"].squeeze(0),
            "attention_mask": inputs["attention_mask"].squeeze(0),
            "labels": inputs["labels"].squeeze(0),
        }

    # Apply preprocessing to the dataset
    return dataset.map(preprocess, remove_columns=["image", "instruction", "expected_output", "image_file"])

# Step 3: Main script
if __name__ == "__main__":
    # Path to the dataset folder
    dataset_path = "./turing_tumble_dataset"

    # Load the dataset
    dataset = load_turing_tumble_dataset(dataset_path)

    # Load the processor for the VILA model
    processor = AutoProcessor.from_pretrained("nvidia/vila")

    # Preprocess the dataset
    processed_dataset = preprocess_dataset(dataset, processor)

    # Save the processed dataset for later use
    processed_dataset.save_to_disk("./processed_turing_tumble_dataset")

    print("Dataset loaded and preprocessed successfully!")