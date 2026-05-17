import re
from transformers import BartForConditionalGeneration, BartTokenizer

print("Loading your fine-tuned model...")
model = BartForConditionalGeneration.from_pretrained("./finetuned-bart")
tokenizer = BartTokenizer.from_pretrained("./finetuned-bart")
print("Model loaded!")

def split_into_chunks(text, max_words=120):
    # Split text into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        
        # If adding this sentence exceeds limit, save chunk and start new one
        if current_word_count + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = word_count
        else:
            current_chunk.append(sentence)
            current_word_count += word_count

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_text(text):
    chunks = split_into_chunks(text, max_words=120)
    
    print(f"Processing {len(chunks)} chunks...")
    
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        
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