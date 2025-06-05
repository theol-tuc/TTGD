from parts.constants import ItemType
from game_logic import GameBoard
# Import necessary libraries
from transformers import AutoModelForVision2Seq, AutoProcessor, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
from datasets import load_from_disk

def parse_and_apply_commands(board: GameBoard, commands: list[str]):
    for command in commands:
        if "add_component" in command:
            try:
                # جدا کردن type و مختصات
                type_str = command.split("type=ItemType.")[1].split(",")[0].strip()
                x = int(command.split("x=")[1].split(",")[0].strip())
                y = int(command.split("y=")[1].split(")")[0].strip())

                component_type = ItemType[type_str.upper()]
                board.add_component(component_type, x, y)

                print(f"✅ Added {component_type} at ({x}, {y})")
            except Exception as e:
                print(f"❌ Error parsing command '{command}': {e}")

# Step 1: Load the preprocessed dataset
def load_dataset(dataset_path: str):
    """
    Load the preprocessed dataset from disk.

    Args:
        dataset_path (str): Path to the preprocessed dataset.

    Returns:
        DatasetDict: The preprocessed dataset.
    """
    return load_from_disk(dataset_path)

# Step 2: Load the base VILA model and processor
def load_model_and_processor(model_name: str):
    """
    Load the base VILA model and processor.

    Args:
        model_name (str): Name of the pre-trained VILA model.

    Returns:
        tuple: The model and processor.
    """
    model = AutoModelForVision2Seq.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)
    return model, processor

# Step 3: Apply LoRA to the model
def apply_lora(model):
    """
    Apply LoRA to the model for parameter-efficient fine-tuning.

    Args:
        model: The base model.

    Returns:
        The model with LoRA applied.
    """
    lora_config = LoraConfig(
        r=8,  # Low-rank dimension
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],  # Target attention layers
        lora_dropout=0.1,
        bias="none",
        task_type="SEQ_2_SEQ_LM"
    )
    model = get_peft_model(model, lora_config)
    return model

# Step 4: Fine-tune the model
def fine_tune_model(model, dataset, output_dir: str):
    """
    Fine-tune the model using the preprocessed dataset.

    Args:
        model: The model to fine-tune.
        dataset: The preprocessed dataset.
        output_dir (str): Directory to save the fine-tuned model.
    """
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        save_total_limit=2,
        load_best_model_at_end=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        tokenizer=processor.tokenizer,
        data_collator=processor
    )

    trainer.train()
    model.save_pretrained(output_dir)

# Step 5: Main script
if __name__ == "__main__":
    # Paths and model name
    dataset_path = "./processed_turing_tumble_dataset"
    model_name = "nvidia/vila"
    output_dir = "./fine_tuned_vila"

    # Load the dataset
    dataset = load_dataset(dataset_path)

    # Load the model and processor
    model, processor = load_model_and_processor(model_name)

    # Apply LoRA to the model
    model = apply_lora(model)

    # Fine-tune the model
    fine_tune_model(model, dataset, output_dir)

    print(f"Fine-tuned model saved to {output_dir}")
