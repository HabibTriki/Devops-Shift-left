FROM python:3.11-slim

# Copy requirement files if available.
COPY requirements*.txt ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the rest of the source.
COPY . .

# Set a reasonable default command; adjust to match your application entry point.
CMD ["python", "main.py"]
