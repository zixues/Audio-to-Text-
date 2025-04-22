# Audio Transcription API (Flask + Groq Whisper)

This Flask-based API allows users to upload audio files (`.mp3`) and receive accurate transcriptions using the **Whisper Large V3** model via **Groq API**.

---

##  Features
- Upload `.mp3` audio and get text transcription
- Uses **Groq's Whisper API** (faster, low-latency inference)
- Automatic cleanup of temp files
- Verbose JSON response for detailed output (configurable)
- Minimal and efficient Flask server

---

## Tech Stack
- **Flask** – Web API
- **Groq Whisper** – Audio-to-text transcription
- **Requests** – HTTP requests to Whisper API
- **dotenv** – Environment variable handling

---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/whisper-transcriber.git
cd whisper-transcriber
```
### 2. Install Dependencies
```bash
pip install flask python-dotenv requests
```
### 3. 3. Add Environment Variables
```bash
GROQ_API=your_groq_api_key_here
```
---

## Running the App
```bash
python app.py
The server will run on: http://127.0.0.1:5000
```
---

## API Endpoints

### Test Endpoint
```bash
GET /testing
```
---
### Transcription Endpoint
```bash
POST /transcribe
```
#### Request
**Content-Type**: multipart/form-data

**Form field**: file (your .mp3 audio file)

---
## Example
```bash
curl -X POST http://127.0.0.1:5000/transcribe \
  -F "file=@your-audio.mp3"
```
## Response
```bash
{
  "transcription": "This is the transcribed text from your audio."
}

```
---

**Notes
Only .mp3 format supported currently.
Groq API key must be valid and active.
Whisper model used: whisper-large-v3


