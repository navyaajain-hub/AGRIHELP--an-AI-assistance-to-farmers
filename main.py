from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = FastAPI(title="AgroBot Core Engine API")

# 1. Load the Trained CNN Model and Class Names Safely

# Get the directory WHERE main.py is currently saved (which is agrobot_env)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Since main.py, agrobot_cnn_model.h5, and plantvillage dataset are ALL in the same folder, 
# we point directly to BASE_DIR without nesting an extra "agrobot_env" string!
MODEL_PATH = os.path.join(BASE_DIR, "agrobot_cnn_model.keras")
DATASET_DIR = os.path.join(BASE_DIR, "plantvillage dataset", "color")

print(f"🔍 DEBUG: Searching for model at: {MODEL_PATH}")
print(f"🔍 DEBUG: File exists check: {os.path.exists(MODEL_PATH)}")

# Load the structural layers
try:
    if os.path.exists(MODEL_PATH):
        disease_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("🔥 Real TensorFlow model loaded successfully into the backend.")
    else:
        disease_model = None
        print("⚠️ Model file not found at path. Running mock fallback mode.")
except Exception as e:
    disease_model = None
    print(f"⚠️ Failed to load model file format ({e}). Running mock fallback mode.")

try:
    disease_model = tf.keras.models.load_model(MODEL_PATH)
    print("🔥 Real TensorFlow model loaded successfully into the backend.")
except Exception as e:
    disease_model = None
    print(f"⚠️ Warning: Model file not found or couldn't load ({e}). Running mock responses.")

# Dynamically scan folder names in alphabetical order from your dataset
try:
    if os.path.exists(DATASET_DIR):
        # Extracts only the folder names from your plantvillage dataset directory
        CLASS_NAMES = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
        print(f"✅ Dynamically mapped {len(CLASS_NAMES)} classes directly from the dataset directory.")
    else:
        CLASS_NAMES = []
        print("⚠️ Warning: Dataset directory not found. Prediction naming might fallback to raw indexes.")
except Exception as e:
    CLASS_NAMES = []
    print(f"⚠️ Error parsing class directories: {e}")


# --- Real Image Preprocessing Helper ---
def preprocess_image(image_bytes: bytes):
    # Convert raw bytes into a PIL Image, ensure RGB format
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Resize to match target CNN input dimensions
    img = img.resize((224, 224))
    img_array = np.array(img)
    # Expand dimensions to create a batch size of 1: shape becomes (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# 2. Add the Image Prediction Endpoint
@app.post("/api/predict")
async def predict_crop_disease(file: UploadFile = File(...)):
    if disease_model is None:
        # Change the mock string here temporarily just to test if you are stuck on mock mode!
        return {"disease": "Stuck on Mock Dropdown Mode", "confidence": "0.0%"}
        
    try:
        # 1. Read and transform the raw file data stream
        image_content = await file.read()
        processed_img = preprocess_image(image_content)
        
        # 2. Run inference through MobileNetV3
        predictions = disease_model.predict(processed_img)
        
        # 3. MobileNet outputs an array of raw prediction values. Find the maximum index.
        top_idx = np.argmax(predictions[0])
        confidence_score = float(predictions[0][top_idx]) * 100
        
        # 4. Map index to the dataset class label string
        detected_class = CLASS_NAMES[top_idx] if CLASS_NAMES else f"Class_{top_idx}"
        clean_name = detected_class.replace("___", " - ").replace("_", " ")
        
        return {
            "disease": clean_name,
            "confidence": f"{confidence_score:.1f}%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")
    
# --- Keep your existing /api/auth/login and analytics endpoints below ---
@app.post("/api/auth/login")
def login(data: dict):
    if data.get("email") == "user@gmail.com" and data.get("password") == "user123":
        return {"status": "success", "user": {"name": "User", "role": "farmer", "email": data["email"]}}
    raise HTTPException(status_code=401, detail="Unauthorized")