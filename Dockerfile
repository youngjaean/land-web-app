FROM --platform=linux/arm64 python:3.9-slim
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    lsb-release \
    git \
    chromium \
    chromium-driver \
    gcc python3-dev libpq-dev\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# CMD ["flask", "run", "--host=0.0.0.0"]