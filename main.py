from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the DTH IPM Analyzer"}

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"

    # Save uploaded file locally
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Read audio file
        sample_rate, data = wavfile.read(temp_file_path)

        # Normalize to mono if stereo
        if len(data.shape) == 2:
            data = data.mean(axis=1)

        # Find peaks (impacts)
        peaks, _ = find_peaks(data, height=np.max(data) * 0.6, distance=sample_rate * 0.1)

        duration_seconds = len(data) / sample_rate
        impacts_per_minute = (len(peaks) / duration_seconds) * 60

        return JSONResponse(content={
            "filename": file.filename,
            "sample_rate": sample_rate,
            "duration_seconds": round(duration_seconds, 2),
            "impacts_detected": len(peaks),
            "ipm": round(impacts_per_minute, 2)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
