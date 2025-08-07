from fastapi import FastAPI, UploadFile, File
import uvicorn
import librosa
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "IPM Analyzer API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(contents)

    y, sr = librosa.load("temp.wav")
    peaks = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    duration = librosa.get_duration(y=y, sr=sr)
    
    ipm = round(len(peaks) / duration * 60, 2)

    return {"impacts_per_minute": ipm}
