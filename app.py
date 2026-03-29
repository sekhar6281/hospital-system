from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import uvicorn

app = FastAPI(title="Hospital Registry")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      name TEXT, specialty TEXT, timings TEXT)''')
    conn.commit()
    conn.close()

init_db()

class Doctor(BaseModel):
    name: str
    specialty: str
    timings: str

# --- ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "Hospital System is Running!"}

@app.post("/register")
def register(doctor: Doctor):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors (name, specialty, timings) VALUES (?, ?, ?)",
                   (doctor.name, doctor.specialty, doctor.timings))
    conn.commit()
    conn.close()
    return {"message": f"Doctor {doctor.name} added."}

@app.delete("/delete/{doctor_id}")
def delete(doctor_id: int):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()
    return {"message": "Doctor deleted."}

# --- THIS ALLOWS 'python3 app.py' TO WORK ---
if __name__ == "__main__":
    print("Starting Hospital System on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
