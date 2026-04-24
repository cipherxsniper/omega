import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

print("🧠 Omega V20 TRAIN STARTED")

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

dataset = load_dataset("json", data_files="train_data_v20.jsonl")
print("📦 Dataset loaded")

tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(x):
    return tokenizer(x["input"] + x["output"], truncation=True, padding="max_length", max_length=128)

dataset = dataset.map(tokenize)
print("🔄 Tokenization done")

model = AutoModelForCausalLM.from_pretrained(model_name)
print("🧠 Model loaded")

args = TrainingArguments(
    output_dir="./omega_v20_model",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    logging_steps=1,
    save_steps=5,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset["train"]
)

print("🚀 TRAINING STARTING NOW...")
trainer.train()

print("✅ TRAINING COMPLETE")
