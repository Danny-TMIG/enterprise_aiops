FROM ubuntu:24.04 AS cpp-builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y git cmake build-essential

WORKDIR /build
RUN git clone --depth 1 https://github.com .
RUN cmake -B build -DCMAKE_BUILD_TYPE=Release
RUN cmake --build build -j

FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY --from=cpp-builder /build/build/bin/whisper-cli /app/whisper_cpp/build/bin/whisper-cli
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn pydantic
COPY . /app/
EXPOSE 8080
CMD ["uvicorn", "universal_platform.app:app", "--host", "0.0.0.0", "--port", "8080"]
