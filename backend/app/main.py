import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="Bus Demand Prediction API",
    description="API for predicting bus demand and suggesting schedules",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import API routers
from app.api import predictions, locations

# Include routers
app.include_router(predictions.router, prefix="/api", tags=["predictions"])
app.include_router(locations.router, prefix="/api", tags=["locations"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Bus Demand Prediction API",
        "docs_url": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
