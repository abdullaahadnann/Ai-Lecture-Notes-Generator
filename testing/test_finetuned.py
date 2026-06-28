from transformers import BartForConditionalGeneration, BartTokenizer

# Load YOUR fine-tuned model (not the original)
print("Loading your fine-tuned model...")
model = BartForConditionalGeneration.from_pretrained("./finetuned-bart")
tokenizer = BartTokenizer.from_pretrained("./finetuned-bart")
print("Model loaded!")

def generate_notes(text):
    # Tokenize input
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    # Generate summary
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=128,
        min_length=30,
        num_beams=4,        # considers 4 possible outputs, picks best
        early_stopping=True
    )

    # Decode output back to text
    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary

# Test it with a new paragraph it has never seen before
test_paragraph = """
Deep learning is a type of machine learning that uses multiple layers 
of neural networks to learn representations of data. It has revolutionized 
fields like computer vision, speech recognition, and natural language 
processing by automatically learning features from raw data without 
manual feature engineering.
"""

print("\nInput:")
print(test_paragraph)

print("\nGenerated Notes:")
print(generate_notes(test_paragraph))