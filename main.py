from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database Setup
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors 
                     (id INTEGER PRIMARY KEY, name TEXT, specialty TEXT, timings TEXT)''')
    conn.commit()
    conn.close()

init_db()

class Doctor(BaseModel):
    name: str
    specialty: str
    timings: str

@app.post("/register-doctor/")
def register_doctor(doctor: Doctor):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO doctors (name, specialty, timings) VALUES (?, ?, ?)",
                   (doctor.name, doctor.specialty, doctor.timings))
    conn.commit()
    conn.close()
    return {"message": "Doctor registered successfully"}

@app.delete("/delete-doctor/{doctor_id}")
def delete_doctor(doctor_id: int):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()
    return {"message": "Doctor deleted"}

@app.patch("/update-timings/{doctor_id}")
def update_timings(doctor_id: int, new_timings: str):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE doctors SET timings = ? WHERE id = ?", (new_timings, doctor_id))
    conn.commit()
    conn.close()
    return {"message": "Timings updated"}
