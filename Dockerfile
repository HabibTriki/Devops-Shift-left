# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Better layer caching for deps
COPY requirements*.txt ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# 2) Copy the rest
COPY . .

# 3) Ensure Flask binds outwards; adapt if you use something else than Flask
ENV FLASK_ENV=production \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

EXPOSE 5000

# 4) Start command (keep main.py as you have)
CMD ["python", "main.py"]
