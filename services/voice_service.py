# services/voice_service.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import FileResponse
from agents.voice_agent import VoiceAgent
import shutil
import os
import uuid

app = FastAPI()
agent = VoiceAgent()

class SpeakRequest(BaseModel):
    text: str

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    extension = audio.filename.split('.')[-1]
    temp_filename = f"temp_input_{uuid.uuid4().hex}.{extension}"
    with open(temp_filename, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    try:
        text = agent.transcribe(temp_filename)
    finally:
        os.remove(temp_filename)

    return {"text": text}

@app.post("/speak", response_class=FileResponse)
async def speak(request: SpeakRequest):
    output_path = f"temp_output_{uuid.uuid4().hex}.wav"
    agent.speak(request.text, output_path=output_path)
    return FileResponse(output_path, media_type="audio/wav", filename="response.wav")
