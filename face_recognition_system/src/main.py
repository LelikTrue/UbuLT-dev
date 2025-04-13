import uvicorn

def main():
    # Запуск FastAPI сервера для логирования распознавания лиц
    # host="0.0.0.0" - сервер будет доступен со всех сетевых интерфейсов
    # port=8000 - стандартный порт для разработки
    # reload=True - автоматическая перезагрузка при изменении кода (удобно при разработке)
    uvicorn.run(
        "services.webhook:app",  # Путь к приложению: модуль services.webhook, переменная app
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
