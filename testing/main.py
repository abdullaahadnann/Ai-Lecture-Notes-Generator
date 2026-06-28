from speech_to_text import convert_audio_to_text
from summarizer import summarize_text
from notes_formatter import format_notes

def generate_notes_from_audio(audio_path, topic="Lecture Notes"):
    
    print("\nStep 1: Transcribing audio...")
    transcript = convert_audio_to_text(audio_path)
    print("Transcription done!")
    print(f"\nTranscript preview: {transcript[:200]}...")

    print("\nStep 2: Summarizing transcript...")
    summary = summarize_text(transcript)
    print("✅ Summary done!")

    print("\nStep 3: Formatting notes...")
    notes = format_notes(summary, topic=topic)
    print("Notes ready!\n")

    return transcript, summary, notes


if __name__ == "__main__":
    # Test with your sample audio
    transcript, summary, notes = generate_notes_from_audio(
        audio_path="sample.mp3",
        topic="AI Lecture"
    )
    print(notes)