from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

class EmergencyContact(BaseModel):
    name: str
    phone_number: str
    email: str

class User(BaseModel):
    name: str
    age: int
    emergency_contact: List[EmergencyContact]

class Location(BaseModel):
    latitude: float
    longitude: float
    timestamp: str

class Locations(BaseModel):
    locations: List[Location]

class UserLocations(BaseModel):
    user_id: int
    locations: List[Location]

@app.post("/locations/")
async def create_locations(user_locations: UserLocations):
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    
    for location in user_locations.locations:
        cursor.execute('''
            INSERT INTO locations (user_id, latitude, longitude, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_locations.user_id, location.latitude, location.longitude, location.timestamp))
    
    conn.commit()
    conn.close()
    return {"message": "Locations added successfully"}

@app.get("/locations/{user_id}")
async def get_locations(user_id: int):
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT latitude, longitude, timestamp FROM locations WHERE user_id = ? ORDER BY timestamp DESC 
    ''', (user_id,))
    
    locations = cursor.fetchall()
    
    conn.close()
    
    return {"locations": locations}