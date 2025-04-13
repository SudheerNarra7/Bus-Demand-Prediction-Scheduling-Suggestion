CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS prediction_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_location_id INTEGER NOT NULL,
    end_location_id INTEGER NOT NULL,
    time_period TEXT NOT NULL,
    occasion TEXT NOT NULL,
    season TEXT NOT NULL,
    total_predicted_demand INTEGER NOT NULL,
    total_buses_needed INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (start_location_id) REFERENCES locations (id),
    FOREIGN KEY (end_location_id) REFERENCES locations (id)
);

CREATE TABLE IF NOT EXISTS prediction_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_log_id INTEGER NOT NULL,
    time_slot TEXT NOT NULL,
    predicted_demand INTEGER NOT NULL,
    buses_needed INTEGER NOT NULL,
    FOREIGN KEY (prediction_log_id) REFERENCES prediction_logs (id)
);
