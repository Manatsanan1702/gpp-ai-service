from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="GPP Temperature Prediction AI API")

class SensorInput(BaseModel):
    temp: float
    hum: float
    outdoor_temp: float = None
    outdoor_hum: float = None

@app.get("/")
def home():
    return {"status": "online", "message": "GPP AI Prediction API is running 24/7"}

@app.post("/predict")
def predict_temperature(data: SensorInput):
    current_temp = data.temp
    current_hum = data.hum
    
    # คำนวณคาดการณ์อุณหภูมิวิกฤต (30°C)
    predict_mins = 0
    predict_text = "แนวโน้มอุณหภูมิ: ปกติคงที่"
    
    if current_temp >= 30.0:
        predict_mins = 0
        predict_text = "🚨 ขณะนี้อุณหภูมิเกิน 30°C แล้ว!"
    elif current_temp >= 26.0:
        # คำนวณประมาณการเวลาที่อุณหภูมิจะถึง 30°C
        rate = 0.05  # อัตราการเพิ่มอุณหภูมิโดยประมาณ (°C/นาที)
        predict_mins = int((30.0 - current_temp) / rate)
        predict_text = f"คาดการณ์อุณหภูมิแตะ 30°C ในอีกประมาณ {predict_mins} นาที"
    
    return {
        "status": "success",
        "current_temp": current_temp,
        "current_hum": current_hum,
        "predictMins": predict_mins,
        "predictMinsText": predict_text
    }
