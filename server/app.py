from flask import Flask, request, jsonify
import os
import assemblyai as aai
import pdfplumber
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set AssemblyAI API key
aai.settings.api_key = os.getenv('ASSEMBLY_AI_KEY')

# Initialize the Transcriber
transcriber = aai.Transcriber()

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to transcribe audio/video using AssemblyAI
def transcribe_audio_or_video(file_path):
    transcript = transcriber.transcribe(file_path)
    return transcript.text

# Endpoint to handle video/PDF upload and transcribe
@app.route('/convert-and-transcribe', methods=['POST'])
def convert_and_transcribe():
    file = request.files.get('file')
    file_type = request.form.get('file_type')  # Expect "video" or "pdf"
    
    if not file or not file_type:
        return jsonify({"error": "No file or file type provided"}), 400

    # Save the uploaded file temporarily
    file_path = f"./temp/{file.filename}"
    file.save(file_path)

    if file_type == "pdf":
        # Extract text from the PDF using pdfplumber
        pdf_text = extract_text_from_pdf(file_path)
        # Clean up temporary file
        os.remove(file_path)
        return jsonify({"transcript": pdf_text}), 200
    elif file_type == "video":
        # Transcribe the video directly using AssemblyAI
        transcript = transcribe_audio_or_video(file_path)
        # Clean up temporary file
        os.remove(file_path)
        return jsonify({"transcript": transcript}), 200
    else:
        return jsonify({"error": "Unsupported file type. Use 'video' or 'pdf'."}), 400

if __name__ == '__main__':
    # Ensure the temp directory exists
    os.makedirs("./temp", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
