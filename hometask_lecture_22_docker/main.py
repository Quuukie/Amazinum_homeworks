import io
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

model = None
categories = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, categories
    try:
        weights = MobileNet_V2_Weights.DEFAULT
        model = mobilenet_v2(weights=weights)
        model.eval()  

        categories = weights.meta["categories"]
        print("Model and labels loaded successfully via lifespan handler.")
    except Exception as e:
        print(f"Error during startup model loading: {e}")
        raise e
    yield  

    print("Shutting down... Cleaning up resources if necessary.")

app = FastAPI(
    title="Simple Computer Vision API",
    lifespan=lifespan
)

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    ),
])

@app.get("/health", summary="Health Check Endpoint")
def health_check():
    """Verifies that the API service is up and the model is loaded."""
    if model is not None:
        return {"status": "healthy", "model": "MobileNetV2 loaded"}
    else:
        return JSONResponse(
            status_code=503, 
            content={"status": "unhealthy", "reason": "Model not initialized"}
        )

@app.post("/predict", summary="Classify uploaded image")
async def predict(file: UploadFile = File(...)):
    """
    Accepts an image file, runs it through MobileNetV2, 
    and returns the top 3 classification predictions with confidences.
    """
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PNG or JPEG image.")
    
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)  
   
        with torch.no_grad():
            output = model(input_batch)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)

        top3_prob, top3_catid = torch.topk(probabilities, 3)
        
        results = []
        for i in range(top3_prob.size(0)):
            results.append({
                "rank": i + 1,
                "label": categories[top3_catid[i]],
                "confidence": round(float(top3_prob[i]), 4)
            })
            
        return {"filename": file.filename, "predictions": results}

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": f"An error occurred during processing: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)