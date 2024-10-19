from flask import Flask, request, jsonify
import os
import assemblyai as aai
import pdfplumber
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set AssemblyAI API key
aai.settings.api_key = os.getenv('ASSEMBLY_AI_KEY')

# Initialize the Transcriber
transcriber = aai.Transcriber()

# Initialize the LLM (Google Gemini Pro)
llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.environ['GOOGLE_API_KEY_AI'],
    max_tokens=512
)

# Global variable to store transcripts
transcripts = {}

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

    # Generate a unique document ID (use file name without extension)
    doc_id = os.path.splitext(file.filename)[0]

    # Save the uploaded file temporarily
    file_path = f"./temp/{file.filename}"
    file.save(file_path)

    if file_type == "pdf":
        # Extract text from the PDF using pdfplumber
        pdf_text = extract_text_from_pdf(file_path)
        # Store the transcript in the global variable
        transcripts[doc_id] = pdf_text
        # Clean up temporary file
        os.remove(file_path)
        return jsonify({"transcript": pdf_text, "doc_id": doc_id}), 200
    elif file_type == "video":
        # Transcribe the video directly using AssemblyAI
        transcript = transcribe_audio_or_video(file_path)
        # Store the transcript in the global variable
        transcripts[doc_id] = transcript
        # Clean up temporary file
        os.remove(file_path)
        return jsonify({"transcript": transcript, "doc_id": doc_id}), 200
    else:
        return jsonify({"error": "Unsupported file type. Use 'video' or 'pdf'."}), 400

# Endpoint to ask questions based on stored transcripts
@app.route('/ask', methods=['POST'])
@app.route('/ask', methods=['POST'])
def ask_pdf():
    # Get the document ID, question, and character from the request
    doc_id = request.form.get('doc_id')
    question = request.form.get('question')
    character = request.form.get('character')

    if not doc_id or not question:
        return jsonify({"error": "No document ID or question provided"}), 400

    # Load the previously stored transcript using doc_id
    pdf_text = transcripts.get(doc_id)

    if pdf_text is None:
        return jsonify({"error": "No transcript found for the provided document ID"}), 400

    # Create the prompt based on whether the character is provided or not
    if character:
        jon_snow_prompt = f"Answer this question in the context of the following text, in the tone in which {character} would answer: {pdf_text}\nQuestion: {question}"
    else:
        jon_snow_prompt = f"Answer this question in the context of the following text: {pdf_text}\nQuestion: {question}"

    # Use the language model to answer the question
    answer = llm.invoke(jon_snow_prompt)  # Directly get the response as a string

    # Check if the answer is empty or not
    if not answer:
        answer = "I couldn't find an answer to your question."

    return jsonify({"answer": answer}), 200


if __name__ == '__main__':
    # Ensure the temp directory exists
    os.makedirs("./temp", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    