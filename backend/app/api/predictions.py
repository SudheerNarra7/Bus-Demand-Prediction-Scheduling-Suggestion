import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
import joblib
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the router
router = APIRouter()

# Define the models
class PredictionRequest(BaseModel):
    start_location_id: int
    end_location_id: int
    time_period: str  # 'Morning', 'Afternoon', 'Evening', 'Night', 'Full_Day'
    occasion: Optional[str] = 'Regular'
    season: Optional[str] = 'Summer'

class PredictionDetail(BaseModel):
    time_slot: str
    predicted_demand: int
    buses_needed: int

class RouteLocation(BaseModel):
    id: int
    name: str

class Route(BaseModel):
    start: RouteLocation
    end: RouteLocation

class PredictionResponse(BaseModel):
    route: Route
    time_period: str
    occasion: str
    season: str
    predictions: List[PredictionDetail]
    total_predicted_demand: int
    total_buses_needed: int

# Database connection function
def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "bus_demand.db")
    logger.info(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Load the model
def get_model():
    try:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "bus_demand_model.joblib")
        logger.info(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Failed to load prediction model")

# Define time slots for each period
time_period_mapping = {
    'Morning': ['Morning'],
    'Afternoon': ['Afternoon'],
    'Evening': ['Evening'],
    'Night': ['Night'],
    'Full_Day': ['Morning', 'Afternoon', 'Evening', 'Night']
}

# Function to predict demand
def predict_demand(model, start_location, end_location, occasion, season, time):
    # Create a sample input
    sample = pd.DataFrame({
        'Start Location': [start_location],
        'end location': [end_location],
        'occasion': [occasion],
        'season': [season],
        'time': [time]
    })
    
    # Log the input
    logger.info(f"Predicting demand for: {sample.to_dict('records')[0]}")
    
    try:
        # Make prediction
        prediction = model.predict(sample)[0]
        predicted_tickets = round(prediction)
        logger.info(f"Predicted demand: {predicted_tickets} tickets")
        return predicted_tickets
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise

@router.post("/predict", response_model=PredictionResponse)
def predict_bus_demand(
    request: PredictionRequest, 
    conn: sqlite3.Connection = Depends(get_db),
    model = Depends(get_model)
):
    """
    Predict bus demand for a route and time period using the trained machine learning model.
    """
    logger.info(f"Received prediction request: {request}")
    
    # Validate input
    if request.start_location_id == request.end_location_id:
        raise HTTPException(status_code=400, detail="Start and end locations must be different")
    
    # Check if locations exist
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM locations WHERE id = ?", (request.start_location_id,))
    start_location = cursor.fetchone()
    
    if start_location is None:
        raise HTTPException(status_code=404, detail=f"Start location with ID {request.start_location_id} not found")
    
    cursor.execute("SELECT id, name FROM locations WHERE id = ?", (request.end_location_id,))
    end_location = cursor.fetchone()
    
    if end_location is None:
        raise HTTPException(status_code=404, detail=f"End location with ID {request.end_location_id} not found")
    
    if request.time_period not in time_period_mapping:
        raise HTTPException(
            status_code=400, 
            detail=f"Time period must be one of: {', '.join(time_period_mapping.keys())}"
        )
    
    # Get time slots for the requested period
    time_slots = time_period_mapping[request.time_period]
    
    # Make predictions for each time slot
    predictions = []
    for time in time_slots:
        try:
            # Use the trained model to predict demand
            predicted_tickets = predict_demand(
                model,
                request.start_location_id,
                request.end_location_id,
                request.occasion,
                request.season,
                time
            )
            
            # Calculate number of buses needed (assuming each bus can carry 50 passengers)
            bus_capacity = 50
            buses_needed = max(1, round(predicted_tickets / bus_capacity))
            
            predictions.append(PredictionDetail(
                time_slot=time,
                predicted_demand=predicted_tickets,
                buses_needed=buses_needed
            ))
            
            logger.info(f"Prediction for {time}: {predicted_tickets} tickets, {buses_needed} buses")
        except Exception as e:
            logger.error(f"Error making prediction for {time}: {e}")
            raise HTTPException(status_code=500, detail=f"Error making prediction for {time}")
    
    # Sort predictions by demand (highest first)
    predictions.sort(key=lambda x: x.predicted_demand, reverse=True)
    
    # Calculate totals
    total_predicted_demand = sum(p.predicted_demand for p in predictions)
    total_buses_needed = sum(p.buses_needed for p in predictions)
    
    # Log the prediction
    try:
        cursor.execute('''
        INSERT INTO prediction_logs 
        (start_location_id, end_location_id, time_period, occasion, season, 
         total_predicted_demand, total_buses_needed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.start_location_id, 
            request.end_location_id, 
            request.time_period, 
            request.occasion, 
            request.season, 
            total_predicted_demand, 
            total_buses_needed
        ))
        
        prediction_log_id = cursor.lastrowid
        
        # Log prediction details
        for pred in predictions:
            cursor.execute('''
            INSERT INTO prediction_details
            (prediction_log_id, time_slot, predicted_demand, buses_needed)
            VALUES (?, ?, ?, ?)
            ''', (
                prediction_log_id, 
                pred.time_slot, 
                pred.predicted_demand, 
                pred.buses_needed
            ))
        
        # Commit changes
        conn.commit()
        logger.info(f"Prediction logged with ID: {prediction_log_id}")
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")
        # Continue even if logging fails
    
    # Prepare response
    response = PredictionResponse(
        route=Route(
            start=RouteLocation(
                id=start_location['id'],
                name=start_location['name']
            ),
            end=RouteLocation(
                id=end_location['id'],
                name=end_location['name']
            )
        ),
        time_period=request.time_period,
        occasion=request.occasion,
        season=request.season,
        predictions=predictions,
        total_predicted_demand=total_predicted_demand,
        total_buses_needed=total_buses_needed
    )
    
    logger.info(f"Returning prediction response with {len(predictions)} time slots")
    return response

@router.get("/predictions/history", response_model=List[dict])
def get_prediction_history(limit: int = 10, conn: sqlite3.Connection = Depends(get_db)):
    """
    Get prediction history.
    """
    logger.info(f"Fetching prediction history (limit: {limit})")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT pl.id, pl.start_location_id, sl.name as start_location_name, 
               pl.end_location_id, el.name as end_location_name,
               pl.time_period, pl.occasion, pl.season, 
               pl.total_predicted_demand, pl.total_buses_needed, pl.timestamp
        FROM prediction_logs pl
        JOIN locations sl ON pl.start_location_id = sl.id
        JOIN locations el ON pl.end_location_id = el.id
        ORDER BY pl.timestamp DESC
        LIMIT ?
        ''', (limit,))
        
        history = cursor.fetchall()
        logger.info(f"Found {len(history)} prediction history records")
        
        # Convert to list of dicts
        result = []
        for item in history:
            result.append(dict(item))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching prediction history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch prediction history")

@router.get("/model/metrics")
def get_model_metrics():
    """
    Get metrics for the trained machine learning model.
    """
    try:
        # These metrics are from the model training
        metrics = {
            "model_type": "Gradient Boosting Regressor",
            "mean_absolute_error": 10.49,
            "root_mean_squared_error": 13.54,
            "r2_score": 0.5436,
            "training_samples": 800,
            "test_samples": 200,
            "features": [
                "occasion (categorical)",
                "Start Location (numerical)",
                "end location (numerical)",
                "season (categorical)",
                "time (categorical)"
            ],
            "target": "no of tickets",
            "hyperparameters": {
                "learning_rate": 0.01,
                "max_depth": 3,
                "n_estimators": 300
            }
        }
        
        return metrics
    except Exception as e:
        logger.error(f"Error getting model metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model metrics")
