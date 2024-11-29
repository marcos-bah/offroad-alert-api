from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import sqlite3

load_dotenv()

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
        
    # enviar email para os contatos de emergência
    cursor.execute('''
        SELECT name, phone_number, email FROM emergency_contacts WHERE user_id = ?
    ''', (user_locations.user_id,))
    
    contacts = cursor.fetchall()
    
    cursor.execute('''
        SELECT name FROM users WHERE id = ?
    ''', (user_locations.user_id,))
    user_name = cursor.fetchone()[0]
    
    locations = user_locations.locations
    str_locations = ""
    
    for location in locations:
        str_locations += f"\nLatitude: {location.latitude}, Longitude: {location.longitude}, Timestamp: {location.timestamp}"
    
    body = f"User {user_name} is in an emergency. All locations are: {str_locations}"
                   
    for contact in contacts:
        name, phone_number, email = contact
        send_emergency_email(email, "Emergency Alert", body)
    
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


def send_emergency_email(to_email: str, subject: str, body: str):
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")
    
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")