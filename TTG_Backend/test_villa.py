# Test script for VILLA model
import torch
import numpy as np
from PIL import Image
import os
from typing import Dict, List, Tuple
from tqdm import tqdm
from .villa_solver import VILLASolver
from .game_logic import ComponentType

def evaluate_villa_model(
    model_path: str,
    test_data_dir: str,
    output_dir: str
) -> Dict:
    """
    Evaluate the VILLA model on test data
    """
    # Initialize VILLA solver with trained model
    solver = VILLASolver(model_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize metrics
    metrics = {
        'component_accuracy': 0.0,
        'position_error': 0.0,
        'total_samples': 0,
        'component_confusion_matrix': np.zeros((len(ComponentType), len(ComponentType)))
    }
    
    # Process test images
    test_images = [f for f in os.listdir(test_data_dir) if f.endswith(('.jpg', '.png'))]
    progress_bar = tqdm(test_images, desc='Evaluating model')
    
    for image_file in progress_bar:
        image_path = os.path.join(test_data_dir, image_file)
        annotation_path = image_path.replace('.jpg', '.json').replace('.png', '.json')
        
        if not os.path.exists(annotation_path):
            continue
        
        # Analyze image
        result = solver.analyze_image(image_path)
        
        if result['status'] == 'success':
            # Load ground truth
            ground_truth = load_annotation(annotation_path)
            
            # Update metrics
            update_metrics(metrics, result['components'], ground_truth)
            
            # Save visualization
            save_visualization(
                image_path,
                result['components'],
                ground_truth,
                os.path.join(output_dir, f'vis_{image_file}')
            )
    
    # Calculate final metrics
    if metrics['total_samples'] > 0:
        metrics['component_accuracy'] /= metrics['total_samples']
        metrics['position_error'] /= metrics['total_samples']
    
    # Save metrics
    save_metrics(metrics, os.path.join(output_dir, 'metrics.json'))
    
    return metrics

def load_annotation(annotation_path: str) -> List[Dict]:
    """
    Load ground truth annotation from JSON file
    """
    import json
    with open(annotation_path, 'r') as f:
        return json.load(f)

def update_metrics(metrics: Dict, predictions: List[Dict], ground_truth: List[Dict]):
    """
    Update evaluation metrics with predictions and ground truth
    """
    metrics['total_samples'] += 1
    
    # Update component accuracy
    for pred, gt in zip(predictions, ground_truth):
        pred_type = ComponentType[pred['type']].value
        gt_type = ComponentType[gt['type']].value
        metrics['component_confusion_matrix'][gt_type][pred_type] += 1
        
        if pred_type == gt_type:
            metrics['component_accuracy'] += 1
        
        # Update position error
        pred_pos = np.array(pred['position'])
        gt_pos = np.array(gt['position'])
        metrics['position_error'] += np.linalg.norm(pred_pos - gt_pos)

def save_visualization(
    image_path: str,
    predictions: List[Dict],
    ground_truth: List[Dict],
    output_path: str
):
    """
    Save visualization of predictions and ground truth
    """
    from PIL import Image, ImageDraw
    
    # Load image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Draw ground truth (green)
    for comp in ground_truth:
        x, y = comp['position']
        draw.rectangle(
            [x-5, y-5, x+5, y+5],
            outline='green',
            width=2
        )
    
    # Draw predictions (red)
    for comp in predictions:
        x, y = comp['position']
        draw.rectangle(
            [x-5, y-5, x+5, y+5],
            outline='red',
            width=2
        )
    
    # Save visualization
    image.save(output_path)

def save_metrics(metrics: Dict, output_path: str):
    """
    Save evaluation metrics to JSON file
    """
    import json
    
    # Convert numpy arrays to lists
    metrics_copy = metrics.copy()
    metrics_copy['component_confusion_matrix'] = metrics_copy['component_confusion_matrix'].tolist()
    
    with open(output_path, 'w') as f:
        json.dump(metrics_copy, f, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate VILLA model for Turing Tumble')
    parser.add_argument('--model_path', type=str, required=True, help='Path to trained model')
    parser.add_argument('--test_data_dir', type=str, required=True, help='Directory containing test data')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save evaluation results')
    
    args = parser.parse_args()
    
    metrics = evaluate_villa_model(
        args.model_path,
        args.test_data_dir,
        args.output_dir
    )
    
    print("\nEvaluation Results:")
    print(f"Component Accuracy: {metrics['component_accuracy']:.4f}")
    print(f"Average Position Error: {metrics['position_error']:.4f}")
    print("\nComponent Confusion Matrix:")
    print(metrics['component_confusion_matrix']) 