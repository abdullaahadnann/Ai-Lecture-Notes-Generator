import os
from flask import Flask, render_template, request, jsonify
from speech_to_text import convert_audio_to_text
from summarizer import summarize_text
from notes_formatter import format_notes

# ============================================================
# STEP 1 — Create Flask app
# ============================================================
app = Flask(__name__)

# Where uploaded audio files will be saved temporarily
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Only allow these audio file types
ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "webm", "mp4"}

# ============================================================
# STEP 2 — Helper function to check file type
# ============================================================
def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================================
# STEP 3 — Home route (loads the webpage)
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")

# ============================================================
# STEP 4 — Generate notes route (handles the upload)
# ============================================================
@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Get topic from form
        topic = request.form.get("topic", "Lecture Notes")

        # Check if audio file was uploaded
        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        file = request.files["audio"]

        # Check if file is empty
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not supported"}), 400

        # Save the uploaded file temporarily
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Step 1 — Transcribe audio
        print("Transcribing audio...")
        transcript = convert_audio_to_text(filepath)

        # Step 2 — Summarize transcript
        print("Summarizing...")
        summary = summarize_text(transcript)

        # Step 3 — Format into notes
        print("Formatting notes...")
        notes = format_notes(summary, topic=topic)

        # Delete the uploaded file after processing
        os.remove(filepath)

        # Send back the results
        return jsonify({
            "transcript": transcript,
            "summary": summary,
            "notes": notes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# STEP 5 — Run the app
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)