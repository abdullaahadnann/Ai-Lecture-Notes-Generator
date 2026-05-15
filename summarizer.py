from transformers import pipeline

print("Loading summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Model loaded!")

def summarize_text(text):
    # split long text into chunks
    max_chunk = 500
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    
    summaries = []
    
    for chunk in chunks:
        summary = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    final_summary = " ".join(summaries)
    
    return final_summary