import sys
import os
import logging

# Настройка логирования
logging.basicConfig(
    filename='/tmp/wsgi_error.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    logging.info("Запуск WSGI скрипта")
    
    # Добавляем путь к проекту
    path = '/home/tymeer/chat'
    if path not in sys.path:
        sys.path.insert(0, path)
    
    logging.info(f"Добавлен путь: {path}")
    logging.info(f"sys.path: {sys.path}")
    
    # Проверка существования файла app.py
    app_path = os.path.join(path, 'app.py')
    logging.info(f"Проверка файла app.py по пути: {app_path}")
    if os.path.exists(app_path):
        logging.info("Файл app.py найден")
    else:
        logging.error(f"Файл app.py НЕ найден по пути: {app_path}")
    
    # Установка переменных окружения
    os.environ['FLASK_ENV'] = 'production'
    # Важно: установка SERVER_NAME через переменную окружения
    os.environ['PYTHONANYWHERE_HOST'] = 'tymeer.pythonanywhere.com'
    
    # Импортируем Flask-приложение
    from app import app as application
    logging.info("Приложение Flask успешно импортировано")
    
    # Проверяем, установлен ли SERVER_NAME
    logging.info(f"SERVER_NAME в конфигурации: {application.config.get('SERVER_NAME', 'Не установлен')}")
    
except Exception as e:
    logging.error(f"Ошибка при инициализации WSGI: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())
    # Создаем простое приложение для отладки
    def application(environ, start_response):
        status = '200 OK'
        output = b'WSGI error! Check logs at /tmp/wsgi_error.log'
        response_headers = [('Content-type', 'text/plain'),
                           ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
