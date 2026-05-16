import json
import torch
from transformers import BartForConditionalGeneration, BartTokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset

# ============================================================
# STEP 1 — Load your dataset
# ============================================================
with open("dataset.json", "r") as f:
    data = json.load(f)

print(f"Loaded {len(data)} examples from dataset.json")

# ============================================================
# STEP 2 — Load BART model and tokenizer
# ============================================================
print("Loading BART model and tokenizer...")
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
print("Model loaded!")

# ============================================================
# STEP 3 — Create a custom Dataset class
# ============================================================
# This tells PyTorch how to read your data during training
class LectureDataset(Dataset):
    def __init__(self, data, tokenizer, max_input=512, max_target=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_input = max_input
        self.max_target = max_target

    def __len__(self):
        # Returns total number of examples
        return len(self.data)

    def __getitem__(self, idx):
        # Gets one example at a time during training
        item = self.data[idx]

        # Tokenize input text (lecture paragraph)
        inputs = self.tokenizer(
            item["input_text"],
            max_length=self.max_input,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Tokenize target text (summary)
        targets = self.tokenizer(
            item["target_text"],
            max_length=self.max_target,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Labels are the tokenized target
        # We replace padding token id with -100 so model ignores padding
        labels = targets["input_ids"].squeeze()
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": labels
        }

# ============================================================
# STEP 4 — Split data into train and test sets
# ============================================================
# 80% training, 20% testing
split = int(0.8 * len(data))
train_data = data[:split]   # first 20 examples
test_data = data[split:]    # last 5 examples

train_dataset = LectureDataset(train_data, tokenizer)
test_dataset = LectureDataset(test_data, tokenizer)

print(f"Training examples: {len(train_dataset)}")
print(f"Testing examples:  {len(test_dataset)}")

# ============================================================
# STEP 5 — Set training settings
# ============================================================
training_args = TrainingArguments(
    output_dir="./finetuned-bart",   # where to save the model
    num_train_epochs=3,              # go through data 3 times
    per_device_train_batch_size=2,   # process 2 examples at once
    per_device_eval_batch_size=2,
    warmup_steps=5,                  # gradually increase learning rate
    weight_decay=0.01,               # prevent overfitting
    logging_dir="./logs",            # save training logs
    logging_steps=5,                 # print loss every 5 steps
    eval_strategy="epoch",           # evaluate after each epoch
    save_strategy="epoch",           # save model after each epoch
    load_best_model_at_end=True,     # keep the best version
)

# ============================================================
# STEP 6 — Create Trainer and start training
# ============================================================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

print("Starting fine-tuning... this will take a while!")
print("You will see the loss printed every 5 steps.")
print("Loss should go DOWN over time — that means the model is learning.")
trainer.train()

# ============================================================
# STEP 7 — Save the fine-tuned model
# ============================================================
print("Saving fine-tuned model...")
model.save_pretrained("./finetuned-bart")
tokenizer.save_pretrained("./finetuned-bart")
print("Done! Your fine-tuned model is saved in the finetuned-bart folder.")