# Use NVIDIA CUDA base image with PyTorch
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git wget curl python3 python3-pip ffmpeg libgl1 libglib2.0-0 build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy repo into container
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install torch>=2.4.0 torchvision>=0.19.0 torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install packaging
RUN pip3 install --no-build-isolation -r requirements.txt

# Expose API port
EXPOSE 8000

# Add a simple FastAPI server wrapper
# (this file you’ll create as server.py)
CMD ["python3", "server.py"]