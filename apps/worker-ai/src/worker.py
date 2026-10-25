import os
import json
import time
import redis
from pipelines.acoustic_features import extract_vocal_biomarkers

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_NAME = "voice_analysis_queue"

def start_worker():
    print(f"[Worker-AI] Conectando a Redis en: {REDIS_URL}")
    r = redis.from_url(REDIS_URL, decode_responses=True)
    print(f"[Worker-AI] Esperando tareas en la cola '{QUEUE_NAME}'...")

    while True:
        try:
            # Bloquea hasta 5 segundos esperando una tarea en la lista
            task_data = r.brpop(QUEUE_NAME, timeout=5)
            if not task_data:
                continue

            _, message_raw = task_data
            job = json.loads(message_raw)
            job_id = job.get("job_id")
            print(f"[Worker-AI] Procesando trabajo {job_id} para paciente {job.get('patient_id')}")

            # En entorno real, aquí se descarga el audio desde el Storage / S3 / R2
            # Para la validación del pipeline inicial registramos el estado:
            results = {
                "job_id": job_id,
                "patient_id": job.get("patient_id"),
                "session_id": job.get("session_id"),
                "processed_at": time.time(),
                "biomarkers": {
                    "f0_mean_hz": 128.45,
                    "jitter_percent": 0.42,
                    "shimmer_percent": 2.15,
                    "hnr_db": 22.8
                },
                "status": "ready"
            }

            # Guardar el resultado en Redis bajo la clave del trabajo
            r.set(f"job_result:{job_id}", json.dumps(results), ex=86400)
            print(f"[Worker-AI] Trabajo {job_id} finalizado y almacenado con éxito.")

        except Exception as e:
            print(f"[Worker-AI] Error durante el procesamiento: {e}")
            time.sleep(2)

if __name__ == "__main__":
    start_worker()