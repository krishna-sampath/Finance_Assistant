# agents/voice_agent.py

import whisper
from TTS.api import TTS

class VoiceAgent:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

    def transcribe(self, audio_path="input.wav"):
        """
        Transcribes speech from an audio file into text.
        """
        result = self.whisper_model.transcribe(audio_path)
        return result["text"]

    def speak(self, text: str, output_path: str = "output.wav"):
        """
        Converts text to speech and saves it as an audio file.
        """
        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path

# Optional: Standalone test
if __name__ == "__main__":
    agent = VoiceAgent()
    text = agent.transcribe("sample_input.wav")
    print("Transcription:", text)
    agent.speak("This is a test of the TTS system.")
