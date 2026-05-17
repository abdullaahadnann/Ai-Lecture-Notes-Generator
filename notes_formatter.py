import re

def generate_title(summary):
    # Extract first sentence to guess topic
    first_sentence = summary.split('.')[0].strip()
    
    # Pull out key nouns/concepts (just take first 4-6 meaningful words)
    words = first_sentence.split()
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "and", "or", 
                  "but", "in", "on", "at", "to", "for", "of", "with", "that",
                  "this", "it", "by", "as", "be", "has", "have", "had", "not",
                  "from", "what", "if", "you", "your", "we", "our", "i", "my"}
    
    key_words = [w.strip('.,!?') for w in words if w.lower().strip('.,!?') not in stop_words]
    
    title = " ".join(key_words[:5]).title()
    
    return title if title else "Lecture Notes"


def format_notes(summary, topic=""):
    
    # ============================================================
    # STEP 1 — Decide title
    # ============================================================
    if topic.strip():
        title = topic          # use what user typed
    else:
        title = generate_title(summary)   # auto generate from content
    
    # ============================================================
    # STEP 2 — Clean up the text
    # ============================================================
    summary = summary.strip()
    summary = re.sub(r'\s+', ' ', summary)
    
    # ============================================================
    # STEP 3 — Split summary into individual sentences
    # ============================================================
    sentences = re.split(r'(?<=[.!?])\s+', summary)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # ============================================================
    # STEP 4 — Extract key terms
    # ============================================================
    key_terms_list = [
        "neural network", "machine learning", "deep learning",
        "supervised", "unsupervised", "reinforcement",
        "training", "model", "algorithm", "dataset",
        "accuracy", "prediction", "classification",
        "natural language", "computer vision", "transformer",
        "gradient descent", "overfitting", "underfitting",
        "tokenizer", "weights", "backpropagation"
    ]
    
    found_terms = []
    summary_lower = summary.lower()
    for term in key_terms_list:
        if term in summary_lower:
            found_terms.append(term.title())
    
    # ============================================================
    # STEP 5 — Build the formatted notes
    # ============================================================
    lines = []
    
    lines.append(f"📌 Topic: {title}")
    lines.append("=" * 40)
    
    lines.append("\n📝 Key Points:")
    for sentence in sentences:
        if not sentence.endswith('.'):
            sentence += '.'
        lines.append(f"  • {sentence}")
    
    if found_terms:
        lines.append("\n🔑 Key Terms:")
        for term in found_terms:
            lines.append(f"  - {term}")
    
    lines.append("\n" + "=" * 40)
    lines.append(f"📊 {len(sentences)} key points extracted")
    
    return "\n".join(lines)

# Test it
if __name__ == "__main__":
    test_summary = "Neural networks mimic the human brain using layers of connected neurons with adjustable weights. They learn to recognize patterns through a process called backpropagation. Deep learning uses multiple layers to solve complex problems like computer vision and natural language processing."
    
    # Test with manual topic
    print("--- WITH MANUAL TOPIC ---")
    print(format_notes(test_summary, topic="Neural Networks"))
    
    print("\n--- WITHOUT TOPIC (auto generated) ---")
    print(format_notes(test_summary, topic=""))