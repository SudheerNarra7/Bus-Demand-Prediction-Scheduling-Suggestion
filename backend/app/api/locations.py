import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the router
router = APIRouter()

# Define the Location model
class Location(BaseModel):
    id: int
    name: str
    description: str = None

# Database connection function
def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "bus_demand.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@router.get("/locations", response_model=List[Location])
def get_locations(conn: sqlite3.Connection = Depends(get_db)):
    """
    Get all available bus locations.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM locations ORDER BY id")
    locations = cursor.fetchall()
    
    return [Location(id=loc['id'], name=loc['name'], description=loc['description']) for loc in locations]

@router.get("/locations/{location_id}", response_model=Location)
def get_location(location_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """
    Get a specific location by ID.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM locations WHERE id = ?", (location_id,))
    location = cursor.fetchone()
    
    if location is None:
        raise HTTPException(status_code=404, detail=f"Location with ID {location_id} not found")
    
    return Location(id=location['id'], name=location['name'], description=location['description'])
