# Simple Computer Vision Inference API

## Overview
This project delivers a lightweight, production-ready computer vision inference service using **FastAPI** and **PyTorch**. The service hosts a pre-trained **MobileNetV2** architecture trained on the ImageNet dataset. Users can upload an image through a RESTful API endpoint and receive the top-3 classification categories alongside their corresponding confidence scores in real-time.

---

## Deployment Info
The application is structured to run as a high-performance web API via **Uvicorn**, an ASGI web server implementation. 

* **Host Environment:** Local machine, Docker container, or cloud virtual machines (AWS EC2, GCP Compute Engine).
* **Server Binding:** `0.0.0.0:8000` (Accessible locally and externally over the assigned network port).
* **Framework Choice:** FastAPI was chosen over Flask due to its native asynchronous support (`async/await`), automatic OpenAPI/Swagger documentation generation, and superior runtime performance.

---

## Installation Instruction

Follow these steps to set up and run the environment locally.

### 1. Prerequisites
Ensure you have **Python 3.9+** installed.

### 2. Setup Environment
Clone or navigate to the solution directory and create a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3.  Install Dependencies
Install the required packages listed in requirements.txt:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.  Run Application
Execute the deployment script to launch the local API server:

```bash
python main.py
#Or if you are trying to run it directly via the Uvicorn CLI instead, use:
uvicorn main:app --reload
```

The server will start up and run at `http://127.0.0.1:8000`

---

## Modeling Info

**Model Architecture**: MobileNetV2 

**Weights Source**: MobileNet_V2_Weights.DEFAULT (PyTorch official pre-trained weights)

**Dataset Target**: ImageNet-1k (1,000 distinct object classes)

**Optimization Strategy**: * The model is locked to evaluation mode (model.eval()) to disable dropout and ensure batch normalization uses running statistics.

*Inference runs within a torch.no_grad() context block to eliminate memory overhead from tracking gradients, boosting execution speed.*

**Input Requirements**: Images are automatically reshaped to 224x224 pixels and normalized using ImageNet channel metrics

---

## Interface Description
Interactive API Documentation

Once the server is running, you can access auto-generated documentation endpoints:

**Swagger UI**: `http://127.0.0.1:8000/docs`

**ReDoc**: `http://127.0.0.1:8000/redoc`

---

## Endpoint Definitions

1. Health check
    * **Endpoint**: GET /health
    * **Description**: Verifies operational readiness of the API and model availability.
    * **Input Format**: None
    * **Output Format (JSON)**:
    ```bash
    {"status": "healthy", ...}
    ```
2. Perform Prediction
    * **Endpoint**: POST /predict
    * **Description**: Processes an image and returns the top 3 class predictions.
    * **Input Format**: An image file (multipart/form-data). Supported formats include JPEG, PNG, etc.
    * **Output**:
    ```bash
    {"filename": "...", "predictions": [...]}
    ```
---

## Example of Processes
Server Logs (Startup & Inference Lifecycle)

When you launch the server and send a request, your console output will log the following pipeline sequence:

```bash
INFO:     Will watch for changes in these directories: ['/Users/dev/cv_deployment_app']
INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [43210] using StatReload
Model and labels loaded successfully.
INFO:     Started server process [43215]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

INFO:     127.0.0.1:54932 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:54945 - "POST /predict HTTP/1.1" 200 OK
```

---

## Client-Side Communication (Request / Response Example)

Using a terminal client like curl, you can query the API with an image file (e.g., an image of a golden retriever):

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@golden_retriever.jpg;type=image/jpeg'
```

## JSON API Output Response:

```bash
{
  "filename": "golden_retriever.jpg",
  "predictions": [
    {
      "rank": 1,
      "label": "golden retriever",
      "confidence": 0.8841
    },
    {
      "rank": 2,
      "label": "Labrador retriever",
      "confidence": 0.0523
    },
    {
      "rank": 3,
      "label": "Irish setter",
      "confidence": 0.0112
    }
  ]
}
```