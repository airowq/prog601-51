import urllib.request
import urllib.error
import json
import time

# Декоратор для логирования времени выполнения
def measure_execution_time(func):
    def internal_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[Время выполнения] Функция '{func.__name__}': {end_time - start_time:.6f} сек")
        return result
    return internal_wrapper

# Функция для создания замыкания с URL API
def create_fetcher(endpoint):
    @measure_execution_time
    def fetch_content():
        try:
            # Выполнение GET запроса с использованием urllib
            with urllib.request.urlopen(endpoint, timeout=3) as response:
                # Проверка статуса ответа
                if response.status != 200:
                    return f"HTTP ошибка: {response.status}"
                
                # Чтение и декодирование ответа
                response_data = response.read().decode('utf-8')
                parsed_data = json.loads(response_data)
                
                # Извлечение информации о факте
                if 'data' in parsed_data and len(parsed_data['data']) > 0:
                    fact_info = parsed_data['data'][0]
                    if 'attributes' in fact_info and 'body' in fact_info['attributes']:
                        return fact_info['attributes']['body']
                    else:
                        return "Не удалось найти текст факта в ответе API"
                else:
                    return "API вернул пустой ответ"
                
        except urllib.error.URLError as error:
            return f"Ошибка URL: {error}"
        except urllib.error.HTTPError as error:
            return f"HTTP ошибка: {error.code} - {error.reason}"
        except json.JSONDecodeError:
            return "Ошибка декодирования JSON ответа"
        except Exception as unexpected_error:
            return f"Непредвиденная ошибка: {unexpected_error}"
    
    return fetch_content

# Альтернативная версия замыкания с повторами
def alternative_requester(api_link):
    @measure_execution_time
    def request_fact(retry_count=1):
        for attempt in range(retry_count):
            try:
                with urllib.request.urlopen(api_link, timeout=2) as response:
                    response_data = response.read().decode('utf-8')
                    parsed_json = json.loads(response_data)
                    
                    # Альтернативный способ извлечения данных
                    fact_text = parsed_json.get('data', [{}])[0].get('attributes', {}).get('body', 'Факт не найден')
                    
                    if fact_text != 'Факт не найден':
                        return fact_text
                    
            except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as error:
                if attempt == retry_count - 1:
                    return f"Не удалось получить факт после {retry_count} попыток: {error}"
                time.sleep(0.5)
        
        return "Не удалось получить данные от API"
    
    return request_fact

# Основная программа
if __name__ == "__main__":
    # Используем URL из задания
    target_url = "https://dogapi.dog/api/v2/facts"
    
    # Создаём первое замыкание
    fact_requester = create_fetcher(target_url)
    
    # Вызываем замыкание для получения факта
    print("\n=== Основное замыкание ===")
    dog_fact = fact_requester()
    print("Полученный факт:", dog_fact)
    
    # Демонстрация альтернативного замыкания
    print("\n=== Альтернативное замыкание (с повторами) ===")
    advanced_requester = alternative_requester(target_url)
    another_fact = advanced_requester(retry_count=2)
    print("Факт из альтернативного замыкания:", another_fact)