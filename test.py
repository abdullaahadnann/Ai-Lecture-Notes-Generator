from speech_to_text import convert_audio_to_text
from summarizer import summarize_text

print("Starting...")

text = convert_audio_to_text("sample.mp3")

print("\nOriginal Text:\n")
print(text)

summary = summarize_text(text)

print("\nSummary:\n")
print(summary)