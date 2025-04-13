# BEGIN: user added these matplotlib lines to ensure any plots do not pop-up in their UI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
import os
os.environ['TERM'] = 'dumb'
# END: user added these matplotlib lines

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
dataset_path = '/Users/sudheerreddynarra/Documents/Projects/bus_demand_prediction_enhanced/backend/app/data/bus_demand_data_cleaned.csv'
model_path = '/Users/sudheerreddynarra/Documents/Projects/bus_demand_prediction_enhanced/backend/app/models/bus_demand_model.joblib'

# Ensure directories exist
os.makedirs('backend/app/models', exist_ok=True)
os.makedirs('backend/app/data', exist_ok=True)

# Load dataset
df = pd.read_csv(dataset_path)

# Features and target
X = df.drop('no of tickets', axis=1)
y = df['no of tickets']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Identify columns
categorical_cols = ['occasion', 'season', 'time']
numerical_cols = ['Start Location', 'end location']

# Preprocessing pipeline
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ('num', StandardScaler(), numerical_cols)
])

# Define models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'AdaBoost': AdaBoostRegressor(random_state=42),
    'ElasticNet': ElasticNet(random_state=42)
}

# Evaluate models
model_results = {}
for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
    model_results[name] = scores.mean()
    logger.info(f"{name} CV R²: {scores.mean():.4f}")

# Select best model
best_model_name = max(model_results, key=model_results.get)
logger.info(f"Best model: {best_model_name}")

# Hyperparameter tuning
param_grid = {}
if best_model_name == 'Random Forest':
    param_grid = {'model__n_estimators': [100, 200], 'model__max_depth': [None, 10, 20]}
elif best_model_name == 'Gradient Boosting':
    param_grid = {'model__n_estimators': [100, 200], 'model__learning_rate': [0.01, 0.1]}
elif best_model_name == 'AdaBoost':
    param_grid = {'model__n_estimators': [50, 100], 'model__learning_rate': [0.1, 1.0]}
elif best_model_name == 'ElasticNet':
    param_grid = {'model__alpha': [0.1, 1.0], 'model__l1_ratio': [0.1, 0.5, 0.9]}

best_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', models[best_model_name])
])

grid_search = GridSearchCV(best_pipeline, param_grid, cv=5, scoring='r2', n_jobs=-1)
grid_search.fit(X_train, y_train)
logger.info(f"Best parameters: {grid_search.best_params_}")

# Final evaluation
y_pred = grid_search.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

logger.info(f"Final Test Evaluation ({best_model_name}):")
logger.info(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}")

# Save model
joblib.dump(grid_search.best_estimator_, model_path)
logger.info(f"Model saved at {model_path}")

# Feature importances for ensemble models
if best_model_name in ['Random Forest', 'Gradient Boosting', 'AdaBoost']:
    feature_names = grid_search.best_estimator_.named_steps['preprocessor'].get_feature_names_out()
    importances = grid_search.best_estimator_.named_steps['model'].feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
    plt.title(f'Feature Importances ({best_model_name})')
    plt.tight_layout()
    plt.savefig('backend/app/models/feature_importances.png')
    logger.info("Feature importance plot saved.")

# Prediction example
def predict_demand(model, start_loc, end_loc, occasion, season, time_of_day):
    sample = pd.DataFrame({
        'occasion': [occasion],
        'season': [season],
        'time': [time_of_day],
        'Start Location': [start_loc],
        'end location': [end_loc]
    })
    prediction = model.predict(sample)[0]
    return round(prediction)

model_loaded = joblib.load(model_path)
test_cases = [
    (1, 5, 'Holiday', 'Summer', 'Morning'),
    (3, 7, 'Regular', 'Winter', 'Evening'),
]

for start, end, occasion, season, time in test_cases:
    tickets = predict_demand(model_loaded, start, end, occasion, season, time)
    logger.info(f"Predicted tickets from {start} to {end} ({occasion}, {season}, {time}): {tickets}")

logger.info("Training and deployment completed.")
