import time
from functools import wraps

# ----- ИЗМЕРИТЕЛЬ ВРЕМЕНИ -----
def measure_time(original_func):
    @wraps(original_func)
    def wrapped(*args, **kwargs):
        start = time.perf_counter()
        output = original_func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMER] Duration: {end - start:.4f} sec.")
        return output
    return wrapped

# ----- ПОСТРОЧНЫЙ ЧИТАТЕЛЬ С РАЗБИЕНИЕМ -----
def make_chunk_reader(filepath, max_chunk_size, encoding='utf-8'):
    """
    Возвращает функцию, которая при каждом вызове отдаёт следующий кусок текста.
    Длинные строки разбиваются на части.
    """
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be positive")
    
    try:
        handle = open(filepath, 'r', encoding=encoding)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except PermissionError:
        print(f"Error: Permission denied for '{filepath}'")
        return None
    except UnicodeDecodeError:
        try:
            handle = open(filepath, 'r', encoding='cp1251')
            print(f"[WARN] Fallback to cp1251 encoding")
        except Exception as e:
            print(f"Error: Cannot read file - {e}")
            return None
    
    leftover = ""
    exhausted = False
    
    def next_chunk():
        nonlocal leftover, exhausted
        
        if exhausted and not leftover:
            return None
        
        if leftover:
            if len(leftover) <= max_chunk_size:
                result = leftover
                leftover = ""
                return result
            else:
                result = leftover[:max_chunk_size]
                leftover = leftover[max_chunk_size:]
                return result
        
        line = handle.readline()
        
        if not line:
            exhausted = True
            handle.close()
            return None
        
        line = line.rstrip('\n\r')
        
        if len(line) <= max_chunk_size:
            return line
        
        result = line[:max_chunk_size]
        leftover = line[max_chunk_size:]
        return result
    
    return next_chunk

# ----- ДЕМОНСТРАЦИЯ -----
if __name__ == "__main__":
    print("=" * 70)
    print("LAB 6: GENERATORS")
    print("=" * 70)
    
    demo_filename = "demo_data.txt"
    demo_content = """Short line.
This is an extremely extremely extremely extremely extremely long line that definitely exceeds the 30 character limit.
Third line with normal length.
Final line of the file."""
    
    with open(demo_filename, 'w', encoding='utf-8') as f:
        f.write(demo_content)
    
    print(f"\n[INFO] Created: {demo_filename}")
    print("-" * 70)
    print(demo_content)
    print("-" * 70)
    
    @measure_time
    def build_reader():
        return make_chunk_reader(demo_filename, max_chunk_size=30)
    
    print("\n[LOG] Initializing reader...")
    reader = build_reader()
    
    if reader is None:
        print("Failed to create reader")
        exit(1)
    
    print("\n[OUTPUT] Reading with 30 char limit:")
    print("-" * 70)
    
    block_no = 1
    while True:
        data = reader()
        if data is None:
            break
        print(f"Block {block_no}: \"{data}\" (len: {len(data)})")
        block_no += 1
    
    print("-" * 70)
    print(f"\n[TOTAL] Blocks read: {block_no - 1}")
    
    print("\n" + "=" * 70)
    print("ADDITIONAL DEMO WITH DIFFERENT LIMITS")
    print("=" * 70)
    
    for limit in [10, 20, 50]:
        print(f"\nLimit: {limit} chars")
        print("-" * 50)
        
        alt_reader = make_chunk_reader(demo_filename, limit)
        if alt_reader:
            idx = 1
            while True:
                text = alt_reader()
                if text is None:
                    break
                print(f"  {idx}: \"{text}\"")
                idx += 1
    
    import os
    os.remove(demo_filename)
    print("\n[INFO] Cleanup complete")