FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_subs.sh .
RUN chmod +x extract_subs.sh

COPY subtitle_extractor.py .
CMD ["python", "-u", "subtitle_extractor.py"]

