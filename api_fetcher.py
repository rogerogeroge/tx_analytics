import requests
import time
import os

# URL к API ручке
API_URL = 'https://app.deguard.io/api/nomis/transactions_deguard/'  # Укажи свой URL API

# API ключ для аутентификации (если требуется)
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibm9taXNfYmU4MTA2NDEtMWI4NS00Y2Q1LTk3ZWYtMGFlNDk0ZTI1ZGU5In0.3dywULNbfr89tgk7FzytZUxABGzszN0eeUkDSVdCUaY'  # Вставь свой API ключ

# Путь к файлу, куда будут сохраняться данные
FILE_PATH = './response.json'

# Функция для запроса данных и сохранения их в файл
def fetch_and_save_data():
    try:
        # Заголовки с API ключом
        headers = {
            'Authorization': f'Bearer MWZlMjcxNTFlYjFmNDc4ZGMxM2Q3ODZhMmU5OTM2YzEwMTgzMzEyYTA5YTA4YjQ1ZDA3MWM1MGNiY2NmN2VmNA==',  # Если используется Bearer токен
            'Content-Type': 'application/json'
        }

        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Проверяем, успешен ли запрос

        # Сохраняем данные в файл response.json
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"Data saved to {FILE_PATH}")
    except Exception as e:
        print(f"Failed to fetch data: {e}")

# Основной цикл, который выполняет запросы каждые 60 секунд
def main():
    while True:
        fetch_and_save_data()
        time.sleep(60)  # Ожидаем 60 секунд перед следующим запросом

if __name__ == "__main__":
    main()
