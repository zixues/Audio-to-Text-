from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from docx import Document
import os
import tempfile
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text
    except Exception as e:
        logging.error(f"Error reading DOCX file: {e}")
        return None

@app.route("/docx-to-audio", methods=["POST"])
def docx_to_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    uploaded_file = request.files["file"]
    
    if not uploaded_file.filename.endswith(".docx"):
        return jsonify({"error": "Invalid file format. Please upload a DOCX file."}), 400
    
    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    uploaded_file.save(temp_file.name)
    temp_file.close()
    
    # Extract text from DOCX
    text = extract_text_from_docx(temp_file.name)
    os.unlink(temp_file.name)  # Remove temporary file
    
    if not text:
        return jsonify({"error": "Failed to extract text from DOCX"}), 500
    
    # Convert text to speech using gTTS
    tts = gTTS(text)
    audio_file = "output.mp3"
    tts.save(audio_file)
    
    return send_file(audio_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
