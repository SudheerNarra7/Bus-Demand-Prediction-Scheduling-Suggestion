# Bus Demand Prediction API Backend

This is the backend API for the Bus Demand Prediction application, built with FastAPI and machine learning.

## Features

- **Machine Learning Model**: Gradient Boosting Regressor trained on bus demand data
- **RESTful API**: FastAPI endpoints for predictions and location data
- **Database**: SQLite database with Texas locations
- **Documentation**: Automatic API documentation with Swagger UI

## Model Performance

- **Mean Absolute Error**: 10.49
- **Root Mean Squared Error**: 13.54
- **R² Score**: 0.5436

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **GET /api/locations**: Get all available locations
- **GET /api/locations/{location_id}**: Get a specific location
- **POST /api/predict**: Make a prediction for bus demand
- **GET /api/predictions/history**: Get prediction history
- **GET /api/model/metrics**: Get model metrics

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Model Details

The machine learning model is a Gradient Boosting Regressor trained on bus demand data. It predicts the number of tickets (demand) based on:

- Start location
- End location
- Occasion (Regular, Weekend, Holiday, etc.)
- Season (Spring, Summer, Fall, Winter)
- Time (Morning, Afternoon, Evening, Night)

The model was trained on 800 samples and tested on 200 samples, achieving an R² score of 0.5436.
