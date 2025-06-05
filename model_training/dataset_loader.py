"""
Dataset loader and preprocessor for fine-tuning VILA on Turing Tumble instructions.
This script handles loading images and JSON annotations, preprocessing them,
and preparing them for the VILA model using Hugging Face's datasets library.
"""

import os
import json
from typing import Dict, List, Union
from pathlib import Path

import torch
from PIL import Image
from datasets import Dataset, DatasetDict, load_dataset
from transformers import (
    AutoProcessor,
    AutoTokenizer,
    ViltProcessor,
    ViltModel,
)

class TuringTumbleDatasetLoader:
    def __init__(
        self,
        data_dir: str,
        model_name: str = "nvidia/vila-1.5-3b",
        max_length: int = 512,
        image_size: tuple = (224, 224),
    ):
        """
        Initialize the dataset loader.
        
        Args:
            data_dir: Directory containing images and JSON annotations
            model_name: Name of the VILA model to use
            max_length: Maximum sequence length for text
            image_size: Target size for images (height, width)
        """
        self.data_dir = Path(data_dir)
        self.model_name = model_name
        self.max_length = max_length
        self.image_size = image_size
        
        # Initialize the VILA processor
        self.processor = AutoProcessor.from_pretrained(model_name)
        
    def load_jsonl_data(self, jsonl_path: str) -> List[Dict]:
        """
        Load JSONL file containing instructions and expected outputs.
        
        Args:
            jsonl_path: Path to the JSONL file
            
        Returns:
            List of dictionaries containing instruction and expected_output
        """
        data = []
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        return data
    
    def load_image(self, image_path: str) -> Image.Image:
        """
        Load and preprocess an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed PIL Image
        """
        image = Image.open(image_path).convert('RGB')
        return image
    
    def prepare_dataset(self, jsonl_path: str) -> Dataset:
        """
        Prepare the dataset by loading images and annotations,
        then processing them for the VILA model.
        
        Args:
            jsonl_path: Path to the JSONL file with annotations
            
        Returns:
            Hugging Face Dataset object ready for training
        """
        # Load annotations
        annotations = self.load_jsonl_data(jsonl_path)
        
        # Prepare dataset dictionary
        dataset_dict = {
            'image_path': [],
            'instruction': [],
            'expected_output': [],
        }
        
        # Process each annotation
        for ann in annotations:
            # Assuming image filename is derived from the annotation
            # You may need to adjust this based on your actual file naming convention
            image_filename = f"{ann['image_id']}.png"  # Adjust based on your naming
            image_path = self.data_dir / image_filename
            
            if image_path.exists():
                dataset_dict['image_path'].append(str(image_path))
                dataset_dict['instruction'].append(ann['instruction'])
                dataset_dict['expected_output'].append(ann['expected_output'])
        
        # Create dataset
        dataset = Dataset.from_dict(dataset_dict)
        
        # Define preprocessing function
        def preprocess_function(examples):
            # Load images
            images = [self.load_image(img_path) for img_path in examples['image_path']]
            
            # Combine instruction and expected output
            texts = [
                f"Instruction: {inst}\nExpected Output: {out}"
                for inst, out in zip(examples['instruction'], examples['expected_output'])
            ]
            
            # Process images and texts using VILA processor
            processed = self.processor(
                images=images,
                text=texts,
                padding='max_length',
                truncation=True,
                max_length=self.max_length,
                return_tensors='pt'
            )
            
            return processed
        
        # Apply preprocessing
        processed_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=dataset.column_names,
            desc="Preprocessing dataset"
        )
        
        return processed_dataset

def main():
    """
    Example usage of the dataset loader.
    """
    # Initialize dataset loader
    # Note: Update these paths based on your actual data location
    data_dir = "path/to/your/data"
    jsonl_path = "path/to/your/annotations.jsonl"
    
    loader = TuringTumbleDatasetLoader(data_dir=data_dir)
    
    # Load and preprocess dataset
    dataset = loader.prepare_dataset(jsonl_path)
    
    # Split into train/validation sets
    dataset_dict = dataset.train_test_split(test_size=0.1)
    
    # Print dataset info
    print("Dataset structure:", dataset_dict)
    print("\nSample processed item:", dataset_dict['train'][0])

if __name__ == "__main__":
    main() 