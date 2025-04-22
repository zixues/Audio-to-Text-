from flask import Flask, request, jsonify
import requests
import tempfile
import logging
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

    
logging.basicConfig(level=logging.DEBUG)

    
WHISPER_API_ENDPOINT = "https://api.groq.com/openai/v1/audio/transcriptions"
WHISPER_API_KEY = os.getenv("GROQ_API")

@app.route("/testing", methods=["GET"])
def test():
    return "This is working"

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    try:
        if "file" in request.files:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            temp_file.write(request.files["file"].read())  
            temp_file.close()
            return jsonify({"transcription": process_audio(file_path=temp_file.name)})
        else:
            return jsonify({"error": "Invalid input. Provide an audio file."}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def process_audio(file_path=None):
    """Process an audio file (local) and return transcription."""
    try:
            
        headers = {"Authorization": f"Bearer {WHISPER_API_KEY}"}
            
            
        with open(file_path, "rb") as audio_file:
            files = {"file": (os.path.basename(file_path), audio_file, "audio/mpeg")}
            data = {"model": "whisper-large-v3", "response_format": "verbose_json", "language": "en"}

            response = requests.post(WHISPER_API_ENDPOINT, headers=headers, files=files, data=data)

        if response.status_code != 200:
            logging.error(f"Whisper API error: {response.text}")
            os.unlink(file_path)
            return {"error": "Failed to get transcription", "details": response.text}

        transcription = response.json().get("text", "")  

        os.unlink(file_path)  

        return transcription  

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)