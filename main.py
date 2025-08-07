from fastapi import FastAPI, UploadFile, File
import librosa
import numpy as np
import tempfile

app = FastAPI()

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    y, sr = librosa.load(tmp_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    return {"estimated_bpm": round(float(tempo[0]), 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
