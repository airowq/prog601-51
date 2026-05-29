import random
import pytest

# ===== БЕСКОНЕЧНЫЙ ПОТОК ДАННЫХ =====
def endless_source(data_pool):
    while True:
        yield random.choice(data_pool)

# ===== ОГРАНИЧЕННЫЙ ИСТОЧНИК =====
def bounded_source(data_pool, upper_bound=5):
    counter = 0
    while counter < upper_bound:
        yield random.choice(data_pool)
        counter += 1

# ===== ЧИСЛОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ =====
def numeric_sequence(limit=10):
    x, y = 0, 1
    step = 0
    while step < limit:
        yield x
        x, y = y, x + y
        step += 1

# ===== ПРОВЕРКИ =====
def verify_endless():
    sample = ["alpha", "beta"]
    gen = endless_source(sample)
    assert isinstance(next(gen), str)

def verify_bounded():
    sample = ["gamma"]
    gen = bounded_source(sample, 3)
    assert len(list(gen)) == 3

def verify_sequence():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert list(numeric_sequence(10)) == expected

if __name__ == "__main__":
    pytest.main([__file__, "-v"])