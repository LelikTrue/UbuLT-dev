# Руководство по развертыванию системы распознавания лиц

## Предварительные требования
- Сервер Ubuntu 22.04 (10.10.101.10)
- Доступ по SSH к серверу
- Python 3.8 или выше установлен на сервере

## Шаг 1: Подготовка серверной среды
1. Подключитесь к серверу по SSH: `ssh user@10.10.101.10`
2. Обновите список пакетов: `sudo apt update`
3. Установите Python и pip: `sudo apt install python3 python3-pip -y`
4. Установите virtualenv: `sudo apt install python3-venv -y`

## Шаг 2: Создание виртуального окружения и установка зависимостей
1. Создайте новый каталог для проекта: `mkdir /opt/face_recognition_system`
2. Создайте виртуальное окружение: `python3 -m venv /opt/face_recognition_system/venv`
3. Активируйте виртуальное окружение: `source /opt/face_recognition_system/venv/bin/activate`

## Шаг 3: Перенос файлов проекта на сервер
1. С локальной машины перенесите файлы проекта на сервер:
   ```bash
   scp -r face_recognition_system user@10.10.101.10:/opt/face_recognition_system/
   ```

## Шаг 4: Настройка переменных окружения
1. Создайте файл `.env` в `/opt/face_recognition_system/` и заполните его необходимыми переменными окружения.

## Шаг 5: Установка зависимостей проекта
1. Перейдите в каталог проекта: `cd /opt/face_recognition_system/face_recognition_system`
2. Установите зависимости: `pip install -r requirements.txt`

## Шаг 6: Запуск приложения
1. Запустите приложение с помощью Uvicorn:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## Шаг 7: Настройка менеджера процессов (необязательно, но рекомендуется)
1. Установите systemd: `sudo apt install systemd -y`
2. Создайте файл службы systemd: `sudo nano /etc/systemd/system/face_recognition.service`
3. Заполните файл службы следующим содержимым:
   ```
   [Unit]
   Description=Face Recognition System
   After=network.target

   [Service]
   User=user
   WorkingDirectory=/opt/face_recognition_system/face_recognition_system
   ExecStart=/opt/face_recognition_system/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
4. Перезагрузите systemd: `sudo systemctl daemon-reload`
5. Включите и запустите службу:
   ```bash
   sudo systemctl enable face_recognition.service
   sudo systemctl start face_recognition.service
   ```

## Дополнительные рекомендации
- Убедитесь, что брандмауэр сервера разрешает трафик на выбранном порту (8000 в этом примере).
- Рассмотрите возможность настройки обратного прокси (например, Nginx) для завершения SSL и дополнительных функций безопасности.
- Регулярно обновляйте зависимости и следите за журналами приложения для выявления проблем.
