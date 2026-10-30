from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from carol_anne.predict import predict, available
from carol_anne.labels import LABELS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Carol_aNNe API is running", "docs": "/docs", "health": "/health", "predict": "POST /predict"}


@app.get("/health")
def health():
    return {"status": "API healthy", "model_loaded": available(), "labels": LABELS}


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if not available():
        raise HTTPException(status_code=503, detail="CNN checkpoint is not loaded")
    audio_bytes = await file.read()
    result = predict(audio_bytes)
    result["filename"] = file.filename
    return result
