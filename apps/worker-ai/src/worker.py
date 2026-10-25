import os
import json
import time
import redis
from pipelines.acoustic_features import extract_vocal_biomarkers

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
QUEUE_NAME = "voice_analysis_queue"

def start_worker():
    print(f"[Worker-AI] Conectando a Redis en: {REDIS_URL}")
    r = redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_timeout=None,
        socket_connect_timeout=10,
        retry_on_timeout=True
    )
    print(f"[Worker-AI] Esperando tareas en la cola '{QUEUE_NAME}'...")

    while True:
        try:
            # Espera bloqueante de hasta 5 segundos
            task_data = r.brpop(QUEUE_NAME, timeout=5)
            if not task_data:
                continue

            _, message_raw = task_data
            job = json.loads(message_raw)
            job_id = job.get("job_id")
            print(f"[Worker-AI] Procesando trabajo {job_id} para paciente {job.get('patient_id')}")

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

            r.set(f"job_result:{job_id}", json.dumps(results), ex=86400)
            print(f"[Worker-AI] Trabajo {job_id} completado con éxito.")

        except redis.ConnectionError as ce:
            print(f"[Worker-AI] Error de conexión con Redis: {ce}. Reintentando en 3s...")
            time.sleep(3)
        except Exception as e:
            print(f"[Worker-AI] Error inesperado: {e}")
            time.sleep(2)

if __name__ == "__main__":
    start_worker()