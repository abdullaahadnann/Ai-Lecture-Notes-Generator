from transformers import BartForConditionalGeneration, BartTokenizer

print("Loading your fine-tuned model...")
model = BartForConditionalGeneration.from_pretrained("./finetuned-bart")
tokenizer = BartTokenizer.from_pretrained("./finetuned-bart")
print("Model loaded!")

def summarize_text(text):
    max_chunk = 500
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    
    summaries = []
    for chunk in chunks:
        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=128,
            min_length=30,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )
        summaries.append(summary)
    
    return " ".join(summaries)