from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
from datetime import datetime
from loguru import logger
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import re
import json

# Создаем FastAPI приложение
app = FastAPI(title="Face Recognition Logger")

# Настройка CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных для события от DVR Agent (для /webhook)
class WebhookEvent(BaseModel):
    name: Optional[str] = None
    timestamp: str
    msg: Optional[str] = None

# Модель данных для эндпоинта /recognition
class RecognitionEvent(BaseModel):
    user_id: str
    full_name: str
    confidence: float
    camera_id: Optional[str] = None
    location: Optional[str] = None

# Создаем директорию для логов
os.makedirs('logs', exist_ok=True)
CSV_LOG_FILE = 'logs/recognition_log.csv'

# Функция для извлечения confidence из msg
def extract_confidence(msg: Optional[str]) -> float:
    if not msg:
        return 0.0
    match = re.search(r"confidence\s+([0-1]\.\d+)", msg, re.IGNORECASE)
    return float(match.group(1)) if match else 0.0

# Функция для записи в CSV
def log_to_csv(full_name: str, timestamp: str):
    file_exists = os.path.isfile(CSV_LOG_FILE)
    try:
        with open(CSV_LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["FullName", "Timestamp"])
            writer.writerow([full_name, timestamp])
        logger.info(f"Данные записаны в CSV: {full_name}, {timestamp}")
    except Exception as e:
        logger.error(f"Ошибка записи в CSV: {str(e)}")
        raise

# Эндпоинт для вебхука от DVR Agent
@app.post("/webhook")
async def receive_webhook(event: WebhookEvent) -> JSONResponse:
    try:
        logger.info(f"Получен вебхук: name={event.name}, timestamp={event.timestamp}, msg={event.msg}")
        confidence = extract_confidence(event.msg)
        if confidence > 0.7:
            full_name = event.name or "Неизвестный"
            try:
                timestamp = datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.warning("Неверный формат timestamp, использована текущая дата")
            log_to_csv(full_name, timestamp)
            response = {
                "status": "success",
                "message": f"Записано распознавание для {full_name}"
            }
            logger.info(f"Ответ вебхука (успех): {response}") # Добавлено логирование
            return JSONResponse(content=response, media_type="application/json; charset=utf-8")
        else:
            logger.info(f"Уверенность ниже порога (0.7): {confidence}, данные не записаны")
            response = {"status": "skipped", "message": "Уверенность ниже порога"}
            logger.info(f"Ответ вебхука (пропущено): {response}") # Добавлено логирование
            return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Обновленный эндпоинт /recognition (пишем в CSV)
@app.post("/recognition")
async def log_recognition_event(event: RecognitionEvent) -> JSONResponse:
    try:
        logger.info(f"Получен запрос на /recognition: user_id={event.user_id}, full_name={event.full_name}, confidence={event.confidence}")
        if event.confidence > 0.7:
            full_name = event.full_name
            # Используем текущую дату, так как timestamp в модели отсутствует
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_csv(full_name, timestamp)
            response = {
                "status": "success",
                "message": f"Записано распознавание для {full_name}"
            }
            logger.info(f"Ответ /recognition (успех): {response}") # Добавлено логирование
            return JSONResponse(content=response, media_type="application/json; charset=utf-8")
        else:
            logger.info(f"Уверенность ниже порога (0.7): {event.confidence}, данные не записаны")
            response = {"status": "skipped", "message": "Уверенность ниже порога"}
            logger.info(f"Ответ /recognition (пропущено): {response}") # Добавлено логирование
            return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Ошибка при обработке события распознавания: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Эндпоинт для чтения логов (оставляем для JSON, но можно адаптировать под CSV)
@app.get("/recognitions")
async def get_recognitions(
    start_date: str = None,
    end_date: str = None,
    user_id: str = None
) -> JSONResponse:
    try:
        events = []
        if os.path.exists('logs/recognitions.json'):
            with open('logs/recognitions.json', 'r', encoding='utf-8') as f:
                for line in f:
                    event = json.loads(line)
                    if user_id and event['user_id'] != user_id:
                        continue
                    if start_date and event['timestamp'] < start_date:
                        continue
                    if end_date and event['timestamp'] > end_date:
                        continue
                    events.append(event)
        return JSONResponse(content={"events": events}, media_type="application/json; charset=utf-8")
    except Exception as e:
        logger.error(f"Ошибка при получении списка распознаваний: {e}")
        raise HTTPException(status_code=500, detail=str(e))
