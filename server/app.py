from flask import Flask, request, jsonify
import os
import assemblyai as aai
import PyPDF2
import pandas as pd
from gtts import gTTS
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set API keys
aai.settings.api_key = os.getenv('ASSEMBLY_AI_KEY')

# Initialize Cloudinary with credentials from .env file
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Initialize the Transcriber
transcriber = aai.Transcriber()

# Function to read PDF and extract text
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to convert PDF text to speech (audio)
def convert_text_to_audio(text, output_path):
    tts = gTTS(text)
    tts.save(output_path)

# Function to extract audio from a video
def extract_audio_from_video(video_path, output_audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_audio_path)

# Function to upload audio to Cloudinary
def upload_audio_to_cloudinary(audio_path):
    response = cloudinary.uploader.upload(audio_path, resource_type="video")  # Upload audio as raw/video
    return response['url']

# Function to transcribe audio using AssemblyAI
def transcribe_audio(audio_path):
    transcript = transcriber.transcribe(audio_path)
    return transcript.text

# Endpoint to handle video/PDF upload, convert to audio, and transcribe
@app.route('/convert-and-transcribe', methods=['POST'])
def convert_and_transcribe():
    file = request.files.get('file')
    file_type = request.form.get('file_type')  # Expect "video" or "pdf"
    
    if not file or not file_type:
        return jsonify({"error": "No file or file type provided"}), 400

    # Save the uploaded file temporarily
    file_path = f"./temp/{file.filename}"
    file.save(file_path)

    # Define paths for temporary audio storage
    audio_path = f"./temp/audio_{os.path.splitext(file.filename)[0]}.mp3"

    # Convert based on the file type
    if file_type == "video":
        # Extract audio from video
        extract_audio_from_video(file_path, audio_path)
    elif file_type == "pdf":
        # Read PDF content and convert text to speech
        pdf_text = read_pdf(file_path)
        convert_text_to_audio(pdf_text, audio_path)
    else:
        return jsonify({"error": "Unsupported file type. Use 'video' or 'pdf'."}), 400

    # Upload the generated audio to Cloudinary (optional)
    audio_url = upload_audio_to_cloudinary(audio_path)

    # Call the transcription API
    transcript = transcribe_audio(audio_path)

    # Clean up temporary files
    os.remove(file_path)
    os.remove(audio_path)

    return jsonify({"transcript": transcript, "audio_url": audio_url}), 200

if __name__ == '__main__':
    # Ensure the temp directory exists
    os.makedirs("./temp", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
