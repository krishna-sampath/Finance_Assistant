import os
import streamlit as st
import requests
import tempfile
from audiorecorder import audiorecorder
from pydub import AudioSegment
from io import BytesIO

# ——— CONFIG ———
ORCH_URL = os.getenv("ORCH_URL", "http://localhost:8006")

st.set_page_config(page_title="🗣️ Market Brief Assistant", layout="wide")
st.title("🗣️ Morning Market Brief")
st.markdown(
    """
    Click **Record**, ask your question out loud (e.g. “What’s our Asia tech exposure?”), 
    then click **Stop**. The app will transcribe, fetch market data, and speak back the summary.
    """
)

# 1) In-browser audio recorder
audio = audiorecorder("🎙️ Record your question")

if audio:
    st.success("Recording complete! Processing…")
    with st.spinner("Generating market brief…"):
        # Convert AudioSegment to WAV bytes
        if hasattr(audio, "export"):  # audio is likely an AudioSegment
            wav_io = BytesIO()
            audio.export(wav_io, format="wav")
            wav_bytes = wav_io.getvalue()
        else:
            st.error("❌ Unsupported audio object.")
            st.stop()

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(wav_bytes)
            tmp_path = tmp.name

        # Send to orchestrator
        files = {"audio": open(tmp_path, "rb")}
        resp = requests.post(f"{ORCH_URL}/run_brief", files=files, stream=True)

        # Clean up input file
        os.remove(tmp_path)

    if resp.status_code != 200:
        st.error(f"❌ Error {resp.status_code}: {resp.text}")
    else:
        # Save the TTS audio response
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as out_tmp:
            for chunk in resp.iter_content(chunk_size=8192):
                out_tmp.write(chunk)
            out_path = out_tmp.name

        st.success("✅ Here’s your market brief:")
        st.audio(out_path, format="audio/wav")
