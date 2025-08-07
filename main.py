from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AudioRequest(BaseModel):
    impacts: int

@app.post("/ipm")
def calculate_ipm(data: AudioRequest):
    # Example: impacts divided by 1 minute (for simplicity)
    return {"ipm": data.impacts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
