# Docker Deployment for an Object Detection API

This project provides a simple computer vision inference API built with FastAPI. It utilizes a pre-trained MobileNetV2 model via PyTorch and Torchvision to classify uploaded images. The application is fully dockerized and configured to allow for flexible execution—you can run the API server or easily execute arbitrary Python scripts and commands inside the container environment.
## Task Requirements

- Create a Docker deployment for a web application.
- Make it possible to run any script inside the container by providing arguments to the docker run command.
- Provide the Dockerfile and screenshots that showcase each step of the process.

## Prerequisites

Docker Desktop must be installed and running.

## Project Structure

```code
.
├── main.py
├── 1.png
├── 2.png
├── 3.png
├── 4.png
├── Dockerfile
├── README.md
├── requirements.txt

```

## Step-by-Step Guide

- ### **Build the Docker Image**
  Navigate to the project's root directory in your terminal and execute the command below.
  This command will read the Dockerfile and build an image containing all dependencies and your application code.

```
docker build -t cv-api .
```

- ### **Run the Web Application**

To run the container in detached mode and make the API available on port 8000, execute:

```
docker run -d -p 8000:8000 --name my-api-container cv-api
```

- ### **Access the API**

Once the container is running successfully, open your browser and navigate to the following address to access the interactive API documentation:

http://localhost:8000/docs

## Task Completion Showcase

Below are the screenshots that confirm the completion of all task requirements.

### Task 1: Create and Run the Docker Deployment

#### Image Build Process

This screenshot shows the successful execution of the docker build command, which creates the cv-api image.
![alt text](1.png)

#### Running Container Logs

After starting the container, the logs show that the model was loaded successfully and the Uvicorn web server has started.
![alt text](2.png)

#### Accessing the Running API via Browser

The web application is successfully deployed and accessible at localhost:8000/docs.
![alt text](3.png)

### Task 2: Running an Arbitrary Command

Execution of a Custom Command
Thanks to the ENTRYPOINT and CMD configuration in the Dockerfile, the default command can be overridden.

The screenshot below shows the execution of arbitrary Python code to print the torch version inside the container.
![alt text](4.png)
Project File Contents

## Dockerfile

```
Dockerfile

# --- Stage 1: Base Image ---

FROM python:3.9-slim

# --- Stage 2: Set Working Directory ---

WORKDIR /app

# --- Stage 3: Install Dependencies ---

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy Application Code ---

COPY main.py .

# --- Stage 5: Expose Port ---

EXPOSE 8000

# --- Stage 6: Configure Entrypoint and CMD ---
ENTRYPOINT ["python"]
CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## requirements.txt

```
fastapi
uvicorn
python-multipart
torch
torchvision
Pillow
```