import re

def format_notes(summary, topic="Lecture Notes"):
    
    # ============================================================
    # STEP 1 — Clean up the text
    # ============================================================
    # Remove extra spaces and newlines
    summary = summary.strip()
    summary = re.sub(r'\s+', ' ', summary)
    
    # ============================================================
    # STEP 2 — Split summary into individual sentences
    # ============================================================
    # Split on period, exclamation, or question mark
    sentences = re.split(r'(?<=[.!?])\s+', summary)
    
    # Remove empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # ============================================================
    # STEP 3 — Extract key terms
    # ============================================================
    # These are important AI/ML words we want to highlight
    key_terms_list = [
        "neural network", "machine learning", "deep learning",
        "supervised", "unsupervised", "reinforcement",
        "training", "model", "algorithm", "dataset",
        "accuracy", "prediction", "classification",
        "natural language", "computer vision", "transformer",
        "gradient descent", "overfitting", "underfitting",
        "tokenizer", "weights", "backpropagation"
    ]
    
    # Find which key terms appear in the summary
    found_terms = []
    summary_lower = summary.lower()
    for term in key_terms_list:
        if term in summary_lower:
            found_terms.append(term.title())
    
    # ============================================================
    # STEP 4 — Build the formatted notes
    # ============================================================
    lines = []
    
    # Title
    lines.append(f"📌 Topic: {topic}")
    lines.append("=" * 40)
    
    # Bullet points from sentences
    lines.append("\n📝 Key Points:")
    for sentence in sentences:
        # Make sure sentence ends with period
        if not sentence.endswith('.'):
            sentence += '.'
        lines.append(f"  • {sentence}")
    
    # Key terms section
    if found_terms:
        lines.append("\n🔑 Key Terms:")
        for term in found_terms:
            lines.append(f"  - {term}")
    
    # Summary line count info
    lines.append("\n" + "=" * 40)
    lines.append(f"📊 {len(sentences)} key points extracted")
    
    return "\n".join(lines)

# Test it
if __name__ == "__main__":
    test_summary = "Neural networks mimic the human brain using layers of connected neurons with adjustable weights. They learn to recognize patterns through a process called backpropagation. Deep learning uses multiple layers to solve complex problems like computer vision and natural language processing."
    
    result = format_notes(test_summary, topic="Neural Networks")
    print(result)