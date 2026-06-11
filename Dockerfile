
FROM python:3.11-slim

# ✅ System settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app  

WORKDIR /app

#  Install system dependencies 
RUN apt-get update && apt-get install -y \
    # build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

#  Install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefer-binary -r requirements.txt

#  Copy project
COPY . .

# ✅ Expose port (HF requirement)
EXPOSE 7860

# Run FastAPI with better logging
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860", "--log-level", "info"]