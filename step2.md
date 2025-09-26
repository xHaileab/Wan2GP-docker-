Prompt for AI Dev: RunPod Hub Metadata & Folder Setup
We’ve cloned the Wan2GP repo and added a Dockerfile + server.py wrapper. Now we need to make this repo RunPod Hub‑ready. Your task is to create the required .runpod/ folder and metadata files so RunPod can build and deploy it as a Serverless API.

✅ Requirements
Create .runpod/ folder at the root of the repo. Inside it, add:

.runpod/hub.json
Purpose: Metadata + deployment hints for RunPod.

Keep it minimal and generic (no repo‑specific assumptions).

Example:

json
{
  "title": "Wan2GP Docker",
  "description": "FastAPI wrapper exposing Wan2GP as a serverless API",
  "type": "serverless",
  "category": "video",
  "config": {
    "runsOn": "GPU",
    "containerDiskInGb": 20,
    "env": []
  }
}
Notes:

title and description are just labels.

category should be "video".

runsOn must be "GPU".

env can stay empty unless we later need secrets or paths.

.runpod/tests.json
Purpose: Defines how RunPod validates the endpoint after deployment.

Example:

json
{
  "tests": [
    {
      "name": "basic_prompt_test",
      "input": {
        "prompt": "Hello world"
      },
      "timeout": 60000
    }
  ],
  "config": {
    "gpuTypeId": "NVIDIA A100",
    "gpuCount": 1,
    "allowedCudaVersions": ["12.1"]
  }
}
Notes:

input should match the FastAPI /generate endpoint fields (e.g., prompt).

Adjust later if we add required inputs like image or video.

gpuTypeId can be "NVIDIA A100" for stability.

🔑 Additional Steps
Handler Script: We already have server.py as the FastAPI entrypoint. No changes needed, but confirm it’s the one RunPod should call.

Badge: Add the RunPod badge to README.md once the Hub build succeeds.

Release: After adding .runpod/ files, commit + push → create a GitHub release (e.g., v0.1.0). RunPod will then build and deploy.

📝 Notes for Dev
Do not assume filenames like wgp.py exist — stick to what’s in the repo (generate.py, etc.).

Keep configs minimal at first. We can expand env or presets later once the endpoint is live.

The goal is just to get RunPod to accept the repo and spin up a working serverless endpoint.