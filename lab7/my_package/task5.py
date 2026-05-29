"""Модуль на основе ЛР №5: API запросы и декоратор"""

import requests
import time
from functools import wraps

# ========== Декоратор для замера времени ==========

def timer_decorator(func):
    """Декоратор, выводящий время выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.4f} сек.")
        return result
    return wrapper

# ========== Замыкание для API запросов ==========

def api_requester(url):
    """
    Замыкание: запоминает URL и возвращает функцию получения факта.
    К внутренней функции применён декоратор timer_decorator.
    """
    @timer_decorator
    def get_fact():
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Пытаемся извлечь факт из разных API
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                # Формат dogapi.dog
                if "attributes" in data["data"][0] and "body" in data["data"][0]["attributes"]:
                    return data["data"][0]["attributes"]["body"]
            # Формат catfact.ninja
            if "fact" in data:
                return data["fact"]
            return str(data)
        except requests.exceptions.RequestException as e:
            return f"Ошибка запроса: {e}"
        except (KeyError, IndexError, ValueError) as e:
            return f"Ошибка парсинга ответа: {e}"
    return get_fact

# ========== Функция для тестирования с разными API ==========

@timer_decorator
def get_fact_from_api(api_name: str):
    """Получить факт из указанного API (dog или cat)"""
    urls = {
        "dog": "https://dogapi.dog/api/v2/facts",
        "cat": "https://catfact.ninja/fact"
    }
    if api_name not in urls:
        return f"Неизвестное API: {api_name}. Доступны: dog, cat"
    
    requester = api_requester(urls[api_name])
    return requester()