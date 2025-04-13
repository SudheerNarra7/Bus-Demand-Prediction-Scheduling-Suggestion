import joblib
import os
import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_model():
    """
    Load the trained machine learning model.
    """
    model_path = os.path.join(os.path.dirname(__file__), "bus_demand_model.joblib")
    logger.info(f"Loading model from {model_path}")
    return joblib.load(model_path)

def predict_demand(model, start_location, end_location, occasion, season, time):
    """
    Predict demand for a specific route and conditions.
    
    Parameters:
    -----------
    model : sklearn.pipeline.Pipeline
        The trained machine learning model
    start_location : int
        The ID of the start location
    end_location : int
        The ID of the end location
    occasion : str
        The occasion (e.g., 'Regular', 'Holiday', 'Weekend')
    season : str
        The season (e.g., 'Summer', 'Winter', 'Spring', 'Fall')
    time : str
        The time of day (e.g., 'Morning', 'Afternoon', 'Evening', 'Night')
        
    Returns:
    --------
    int
        The predicted number of tickets
    """
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
