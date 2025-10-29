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
        "python3", "generate.py",
        "--task", "i2v-A14B",
        "--ckpt_dir", "/app/models",
        "--prompt", prompt,
        "--save_file", output_path
    ]
    if image_path:
        cmd.extend(["--image", image_path])
    if video_path:
        cmd.extend(["--video", video_path])

    subprocess.run(cmd, check=True)

    return {"status": "success", "output": output_path}

if __name__ == "__main__":
    # Download models if they don't exist
    model_dir = "/app/models"
    if not os.path.exists(model_dir):
        print("Downloading models...")
        from huggingface_hub import snapshot_download
        snapshot_download(repo_id="Wan-AI/Wan2.2-I2V-A14B", local_dir=model_dir)
        print("Model download complete.")

    os.makedirs("/app/tmp", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)