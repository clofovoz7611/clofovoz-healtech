FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY apps/worker-ai/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/worker-ai/src ./src

CMD ["python", "src/worker.py"]