import pickle
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .schemas import PredictionInput, PredictionOutput, HealthResponse

# Initialize FastAPI app
app = FastAPI(
    title="Bike Rental Demand Prediction API",
    description="Predict bike rental demand using machine learning",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "bike_rental_model.pkl"
FRONTEND_DIR = BASE_DIR / "frontend"

# Load model at startup
model = None


def load_model():
    """Load the trained model from pickle file"""
    global model
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
    except FileNotFoundError:
        print(f"⚠️ Model not found at {MODEL_PATH}. Run the notebook first to train and save the model.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()


# Mount static files for frontend
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", response_class=FileResponse)
async def root():
    """Serve the frontend"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Bike Rental Prediction API", "docs": "/docs"}


@app.get("/style.css", response_class=FileResponse)
async def get_css():
    """Serve CSS file"""
    css_path = FRONTEND_DIR / "style.css"
    if css_path.exists():
        return FileResponse(str(css_path), media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")


@app.get("/script.js", response_class=FileResponse)
async def get_js():
    """Serve JavaScript file"""
    js_path = FRONTEND_DIR / "script.js"
    if js_path.exists():
        return FileResponse(str(js_path), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Predict bike rental demand based on input features.
    
    - **season**: 1=Spring, 2=Summer, 3=Fall, 4=Winter
    - **yr**: 0=2011, 1=2012
    - **mnth**: Month (1-12)
    - **hr**: Hour (0-23)
    - **holiday**: 0=No, 1=Yes
    - **weekday**: 0=Sunday to 6=Saturday
    - **workingday**: 0=No, 1=Yes
    - **weathersit**: 1=Clear, 2=Mist, 3=Light Rain, 4=Heavy Rain
    - **temp**: Normalized temperature (0-1)
    - **atemp**: Normalized feeling temperature (0-1)
    - **hum**: Normalized humidity (0-1)
    - **windspeed**: Normalized wind speed (0-1)
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please run the notebook first to train and save the model."
        )
    
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data.model_dump()])
        
        # Make prediction
        prediction = model.predict(input_df)
        
        # Return result (ensure non-negative)
        predicted_count = max(0, int(round(prediction[0])))
        
        return PredictionOutput(
            prediction=predicted_count,
            status="success",
            message=f"Predicted {predicted_count} bike rentals"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/features")
async def get_feature_info():
    """Get information about input features"""
    return {
        "season": {"min": 1, "max": 4, "labels": ["Spring", "Summer", "Fall", "Winter"]},
        "yr": {"min": 0, "max": 1, "labels": ["2011", "2012"]},
        "mnth": {"min": 1, "max": 12},
        "hr": {"min": 0, "max": 23},
        "holiday": {"min": 0, "max": 1, "labels": ["No", "Yes"]},
        "weekday": {"min": 0, "max": 6, "labels": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]},
        "workingday": {"min": 0, "max": 1, "labels": ["No", "Yes"]},
        "weathersit": {"min": 1, "max": 4, "labels": ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain"]},
        "temp": {"min": 0, "max": 1, "description": "Normalized (actual_temp / 41)"},
        "atemp": {"min": 0, "max": 1, "description": "Normalized (actual_atemp / 50)"},
        "hum": {"min": 0, "max": 1, "description": "Normalized (actual_hum / 100)"},
        "windspeed": {"min": 0, "max": 1, "description": "Normalized (actual_windspeed / 67)"}
    }
