import os
import json
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis

app = FastAPI(
    title="ClofoVoz Healtech API",
    version="1.0.0",
    description="API Gateway clínica para análisis acústico y biomarcadores vocales"
)

# CORS para el frontend clínico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
queue_client = None

@app.on_event("startup")
def connect_redis():
    global queue_client
    try:
        queue_client = redis.from_url(REDIS_URL, decode_responses=True)
    except Exception as e:
        print(f"Advertencia: No se pudo conectar a Redis: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "clofovozhealtech-api"}

@app.post("/api/v1/audio/analyze")
async def analyze_audio(
    patient_id: str = Form(...),
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(status_code=400, detail="Formato no admitido. Requiere WAV, MP3 u OGG.")

    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "patient_id": patient_id,
        "session_id": session_id,
        "filename": file.filename,
        "status": "queued"
    }

    if queue_client:
        queue_client.lpush("voice_analysis_queue", json.dumps(payload))

    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Audio recibido y remitido al worker de IA acústica"
    }