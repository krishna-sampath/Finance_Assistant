import requests

if __name__ == "__main__":
    with open("input.wav", "rb") as audio_file:
        resp = requests.post(
            "http://localhost:8006/run_brief",  # ensure this matches your orchestrator port
            files={"audio": audio_file}
        )
        if resp.status_code == 200:
            with open("output.wav", "wb") as out_file:
                out_file.write(resp.content)
            print("✅ Output saved as output.wav")
        else:
            print("❌ Error occurred:", resp.status_code, resp.text)