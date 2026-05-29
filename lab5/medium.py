import time
from functools import wraps

# ========== ПРАВИЛЬНЫЙ ДЕКОРАТОР ДЛЯ РЕКУРСИИ ==========
def timer_decorator(active=True, output=True):
    def decorator(func):
        # Флаг хранится ВНЕ wrapper, чтобы не теряться
        recursion_depth = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal recursion_depth
            
            if not active:
                return func(*args, **kwargs)
            
            recursion_depth += 1
            
            if recursion_depth == 1:
                # Первый вызов - замеряем
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                
                if output:
                    print(f"[ДЕКОРАТОР] {func.__name__}: {end - start:.4f} сек.")
                
                wrapper.last_time = end - start
            else:
                # Вложенный рекурсивный вызов - просто выполняем
                result = func(*args, **kwargs)
            
            recursion_depth -= 1
            return result
        return wrapper
    return decorator

# ========== ТЕСТ ==========
@timer_decorator(active=True, output=True)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

if __name__ == "__main__":
    print("Вычисление fib(35)...")
    result = fib(35)
    print(f"fib(35) = {result}")