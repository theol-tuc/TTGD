"""
Preprocessing script for the Turing Tumble dataset.
This script handles:
1. Image resizing and format conversion
2. Dataset splitting
3. Creating processed versions of images
4. Preparing annotations for training
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split

class DatasetPreprocessor:
    def __init__(
        self,
        raw_dir: str = "dataset/raw",
        processed_dir: str = "dataset/processed",
        annotations_dir: str = "dataset/annotations",
        image_size: Tuple[int, int] = (224, 224),
        test_size: float = 0.1,
        random_state: int = 42,
    ):
        """
        Initialize the preprocessor.
        
        Args:
            raw_dir: Directory containing raw images
            processed_dir: Directory for processed images
            annotations_dir: Directory for annotation files
            image_size: Target size for images (height, width)
            test_size: Proportion of data to use for validation
            random_state: Random seed for reproducibility
        """
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.annotations_dir = Path(annotations_dir)
        self.image_size = image_size
        self.test_size = test_size
        self.random_state = random_state
        
        # Create necessary directories
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.annotations_dir.mkdir(parents=True, exist_ok=True)
        
    def process_image(self, image_path: Path) -> np.ndarray:
        """
        Process a single image: resize and convert to RGB.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Processed image as numpy array
        """
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
            
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize
        img = cv2.resize(img, self.image_size, interpolation=cv2.INTER_AREA)
        
        return img
    
    def save_processed_image(self, img: np.ndarray, save_path: Path):
        """
        Save processed image.
        
        Args:
            img: Image as numpy array
            save_path: Path to save the image
        """
        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(save_path), img_bgr)
    
    def collect_annotations(self) -> List[Dict]:
        """
        Collect all annotations from the raw directory.
        
        Returns:
            List of annotation dictionaries
        """
        annotations = []
        image_dir = self.raw_dir / "images"
        
        # Find all JSONL files in the raw directory
        jsonl_files = list(self.raw_dir.glob("*.jsonl"))
        if not jsonl_files:
            raise ValueError("No JSONL files found in raw directory")
            
        # Load annotations from all JSONL files
        for jsonl_file in jsonl_files:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    ann = json.loads(line.strip())
                    # Verify image exists
                    img_path = image_dir / f"{ann['image_id']}.png"
                    if img_path.exists():
                        annotations.append(ann)
        
        return annotations
    
    def split_dataset(self, annotations: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Split annotations into train and validation sets.
        
        Args:
            annotations: List of annotation dictionaries
            
        Returns:
            Tuple of (train_annotations, val_annotations)
        """
        return train_test_split(
            annotations,
            test_size=self.test_size,
            random_state=self.random_state
        )
    
    def save_annotations(self, annotations: List[Dict], split: str):
        """
        Save annotations to JSONL file.
        
        Args:
            annotations: List of annotation dictionaries
            split: 'train' or 'val'
        """
        output_file = self.annotations_dir / f"{split}.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for ann in annotations:
                f.write(json.dumps(ann) + '\n')
    
    def process_dataset(self):
        """
        Main processing function that:
        1. Collects all annotations
        2. Splits into train/val sets
        3. Processes and saves images
        4. Saves annotations
        """
        print("Collecting annotations...")
        annotations = self.collect_annotations()
        
        print("Splitting dataset...")
        train_anns, val_anns = self.split_dataset(annotations)
        
        # Process and save images for each split
        for split, anns in [('train', train_anns), ('val', val_anns)]:
            print(f"\nProcessing {split} set...")
            split_dir = self.processed_dir / split
            split_dir.mkdir(exist_ok=True)
            
            for ann in tqdm(anns, desc=f"Processing {split} images"):
                # Process image
                img_path = self.raw_dir / "images" / f"{ann['image_id']}.png"
                try:
                    img = self.process_image(img_path)
                    # Save processed image
                    save_path = split_dir / f"{ann['image_id']}.png"
                    self.save_processed_image(img, save_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
                    continue
            
            # Save annotations
            self.save_annotations(anns, split)
        
        print("\nPreprocessing complete!")
        print(f"Processed {len(train_anns)} training and {len(val_anns)} validation samples")

def main():
    """
    Run the preprocessing pipeline.
    """
    preprocessor = DatasetPreprocessor()
    preprocessor.process_dataset()

if __name__ == "__main__":
    main() 