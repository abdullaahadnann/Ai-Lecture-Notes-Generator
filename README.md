# AI Lecture Notes Generator 🎤📝

An AI-powered tool that converts lecture audio into structured notes automatically.

## How it works
Audio → Whisper (speech to text) → Fine-tuned BART (summarization) → Structured Notes

## Features
- 🎤 Upload any lecture audio (mp3, wav, m4a)
- 🧠 AI summarization using fine-tuned BART model
- 📝 Structured notes with bullet points and key terms
- 💻 Fully local — no external APIs needed

## Setup

### 1. Clone the repo
git clone https://github.com/abdullaahadnann/AI-Lecture-Notes-Generator.git
cd AI-Lecture-Notes-Generator

### 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install flask openai-whisper transformers torch accelerate datasets

### 4. Generate the fine-tuned model
The model is not uploaded due to its large size. Generate it locally by running:
python finetune.py

This will create the `finetuned-bart` folder with your trained model.

### 5. Run the app
python main.py

## Project Structure
AI Lecture Notes Generator/
│
├── speech_to_text.py     # Whisper audio transcription
├── summarizer.py         # Fine-tuned BART summarization
├── notes_formatter.py    # Structures summary into notes
├── finetune.py           # Fine-tuning script
├── main.py               # Full pipeline
├── dataset.json          # Training dataset (25 examples)
└── README.md

## Models Used
- **Whisper base** — OpenAI's speech recognition model (local)
- **facebook/bart-large-cnn** — Fine-tuned on custom AI lecture dataset

## Tech Stack
- Python
- HuggingFace Transformers
- OpenAI Whisper
- Flask (web UI coming soon)