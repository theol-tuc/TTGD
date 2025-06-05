# Turing Tumble Vision-Language Dataset

This dataset contains screenshots from the Turing Tumble game board paired with corresponding instructions and expected outputs. The dataset is designed for fine-tuning vision-language models like NVIDIA's VILA.

## Directory Structure

```
dataset/
├── raw/                    # Original, unprocessed images
│   └── images/            # All game board screenshots
├── processed/             # Processed images and annotations
│   ├── train/            # Training set
│   └── val/              # Validation set
├── annotations/           # JSONL files
│   ├── train.jsonl       # Training annotations
│   └── val.jsonl         # Validation annotations
```

## Image Format

- All images should be in PNG format
- Recommended image size: 224x224 pixels (will be resized during preprocessing)
- Naming convention: `{scenario}_{state}_{id}.png`
  - Example: `counter_3_before.png`, `counter_3_after.png`
  - `scenario`: The type of puzzle or scenario (e.g., counter, adder)
  - `state`: The state of the board (e.g., before, after)
  - `id`: A unique identifier for the scenario

## Annotation Format

Annotations are stored in JSONL format (one JSON object per line). Each line contains:

```json
{
    "image_id": "counter_3_before",  // Matches the image filename without extension
    "instruction": "Describe the current state of the board and what needs to be done",
    "expected_output": "The board shows a counter setup with 3 blue marbles. We need to add a mechanism to count up to 5."
}
```

## Dataset Usage

1. Place your original images in `dataset/raw/images/`
2. Create annotation files in `dataset/annotations/`
3. Run the preprocessing script to generate the processed dataset
4. Use the dataset loader (`model_training/dataset_loader.py`) to load the data for training

## Adding New Data

1. Add new images to `dataset/raw/images/` following the naming convention
2. Add corresponding annotations to the appropriate JSONL file in `dataset/annotations/`
3. Run preprocessing to update the processed dataset

## Preprocessing

The preprocessing script will:
1. Resize images to the target size
2. Convert images to RGB format
3. Generate train/validation splits
4. Create processed versions of the images
5. Prepare the data for model training 