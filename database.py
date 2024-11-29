# FILE: database.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emergency_contacts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            latitude REAL,
            longitude REAL,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', ('Default User', 30))
    
    user_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO emergency_contacts (user_id, name, phone_number, email) VALUES (?, ?, ?, ?)
    ''', (user_id, 'Default Contact', '+5535997398200', 'marcos.barbosa@unifei.edu.br'))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()