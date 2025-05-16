import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from llava.model import LlavaLlamaForCausalLM
from llava.conversation import conv_templates
from llava.mm_utils import process_images
from PIL import Image
import argparse

def download_llava_model(model_path: str = "llava-v1.5-13b"):
    """Download and set up the LLaVA model"""
    print(f"Setting up LLaVA model at {model_path}")
    
    # Create model directory if it doesn't exist
    os.makedirs(model_path, exist_ok=True)
    
    try:
        # Download model and tokenizer
        print("Downloading model and tokenizer...")
        model = LlavaLlamaForCausalLM.from_pretrained(
            "liuhaotian/llava-v1.5-13b",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained("liuhaotian/llava-v1.5-13b")
        
        # Save model and tokenizer
        print("Saving model and tokenizer...")
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
        
        print("LLaVA model setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up LLaVA model: {str(e)}")
        return False

def test_llava_model(model_path: str = "llava-v1.5-13b"):
    """Test the LLaVA model with a sample image"""
    try:
        # Load model and tokenizer
        print("Loading model and tokenizer...")
        model = LlavaLlamaForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Create a sample image (you can replace this with your own test image)
        print("Creating test image...")
        test_image = Image.new('RGB', (224, 224), color='white')
        
        # Process image
        print("Processing image...")
        image_tensor = process_images([test_image], model.config)
        
        # Create conversation
        conv = conv_templates["llava_v1"].copy()
        conv.append_message(conv.roles[0], "Describe what you see in this image.")
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()
        
        # Generate response
        print("Generating response...")
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                do_sample=True,
                temperature=0.7,
                max_new_tokens=512,
                use_cache=True,
            )
        
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        print("\nTest Response:")
        print(response.split("ASSISTANT:")[-1].strip())
        
        print("\nLLaVA model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing LLaVA model: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Set up and test LLaVA model")
    parser.add_argument("--model_path", type=str, default="llava-v1.5-13b",
                      help="Path to save/load the LLaVA model")
    parser.add_argument("--test_only", action="store_true",
                      help="Only test the model without downloading")
    args = parser.parse_args()
    
    if not args.test_only:
        success = download_llava_model(args.model_path)
        if not success:
            print("Failed to set up LLaVA model")
            return
    
    success = test_llava_model(args.model_path)
    if not success:
        print("Failed to test LLaVA model")
        return
    
    print("\nLLaVA model is ready to use!")

if __name__ == "__main__":
    main() 