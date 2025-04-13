# Face Recognition Logger

Сервис для логирования результатов распознавания лиц от DVR Agent и CodeProjectAI.

## Структура проекта

```
face_recognition_system/
│
├── src/
│   ├── services/
│   │   └── webhook.py     # Сервис логирования
│   └── main.py           # Точка входа
│
├── logs/                 # Логи распознавания
│   └── recognitions.json # Результаты распознавания
│
└── requirements.txt      # Зависимости Python
```

## Установка

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # для Windows
   source venv/bin/activate  # для Linux/Mac
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервис:
   ```bash
   python src/main.py
   ```
   Сервис запустится на http://0.0.0.0:8000

## API Endpoints

### Логирование распознавания
POST `/recognition`
- Вход: JSON с данными распознавания
  ```json
  {
    "user_id": "123",
    "full_name": "Иванов Иван",
    "confidence": 0.95,
    "camera_id": "cam1",
    "location": "Вход"
  }
  ```
- Выход: Подтверждение записи

### Просмотр логов
GET `/recognitions`
- Параметры:
  - `user_id`: Фильтр по ID пользователя
  - `start_date`: Начальная дата (ISO формат)
  - `end_date`: Конечная дата (ISO формат)
- Выход: Список событий распознавания

## Примеры использования

### Python
```python
import requests

# Логирование распознавания
response = requests.post(
    "http://localhost:8000/recognition",
    json={
        "user_id": "123",
        "full_name": "Иванов Иван",
        "confidence": 0.95,
        "camera_id": "cam1",
        "location": "Вход"
    }
)

# Получение списка распознаваний
response = requests.get(
    "http://localhost:8000/recognitions",
    params={"user_id": "123"}
)
```

### curl
```bash
# Логирование распознавания
curl -X POST http://localhost:8000/recognition \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123",
    "full_name": "Иванов Иван",
    "confidence": 0.95,
    "camera_id": "cam1",
    "location": "Вход"
  }'

# Получение списка распознаваний
curl "http://localhost:8000/recognitions?user_id=123"
```
