Ultimate Dockerization Prompt for Wan2GP
Create a file called Dockerfile in the root of your cloned repo with this content:

dockerfile
# Use NVIDIA CUDA base image with PyTorch
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git wget curl python3 python3-pip ffmpeg libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy repo into container
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Expose API port
EXPOSE 8000

# Add a simple FastAPI server wrapper
# (this file you’ll create as server.py)
CMD ["python3", "server.py"]
🖥️ Add a Minimal API Wrapper (server.py)
Inside your repo, create a file called server.py:

python
from fastapi import FastAPI, UploadFile, Form
import uvicorn
import subprocess
import os

app = FastAPI()

@app.post("/generate")
async def generate_video(
    prompt: str = Form(...),
    image: UploadFile = None,
    video: UploadFile = None
):
    # Save inputs
    if image:
        image_path = f"/app/tmp/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())
    else:
        image_path = None

    if video:
        video_path = f"/app/tmp/{video.filename}"
        with open(video_path, "wb") as f:
            f.write(await video.read())
    else:
        video_path = None

    # Call Wan2GP script (adjust to match repo entrypoint)
    output_path = "/app/tmp/output.mp4"
    cmd = [
        "python3", "wgp.py",
        "--prompt", prompt,
        "--output", output_path
    ]
    if image_path:
        cmd.extend(["--image", image_path])
    if video_path:
        cmd.extend(["--video", video_path])

    subprocess.run(cmd, check=True)

    return {"status": "success", "output": output_path}

if __name__ == "__main__":
    os.makedirs("/app/tmp", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)