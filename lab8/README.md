# Лабораторная работа №8: GUI приложение "Meme Generator"

## Условие задачи (Rare)

Разработать приложение с графическим интерфейсом для создания мемов:
- Загрузка изображения
- Добавление верхнего и нижнего текста
- Настройка размера, цвета текста и обводки
- Предпросмотр и сохранение результата

## Условие задачи (Medium)

Модернизировать приложение, добавив:
- Выбор шрифта
- Прозрачность текста
- Поворот текста
- Позиционирование текста (центр/лево/право/произвольно)
- Тень текста
- Фильтры изображения (ч/б, сепия, контраст, яркость)
- История действий (отмена/повтор)
- Горячие клавиши
- Экспорт в PNG/JPG

---

## Описание проделанной работы

### 1. Архитектура приложения

Приложение построено на принципе **разделения ответственности**:

| Компонент | Ответственность |
|-----------|-----------------|
| `MemeCore` | Работа с изображениями (загрузка, фильтры, наложение текста) |
| `HistoryManager` | Управление историей действий (отмена/повтор) |
| `TextStyler` | Настройки текста (цвет, шрифт, прозрачность, поворот) |
| `ImageProcessor` | Фильтры и трансформации изображений |
| `MemeGeneratorPro` | GUI и связь между компонентами |

### 2. Ключевые реализации

#### Делегирование операций (паттерн "Композиция")

Вместо монолитного класса, функционал разнесён по отдельным классам:

```python
class MemeCore:
    """Ядро приложения: хранение и базовые операции с изображением"""
    def __init__(self):
        self._original = None
        self._current = None
        self._history = []
    
    def load(self, path):
        self._original = Image.open(path)
        self._current = self._original.copy()
    
    def apply_filter(self, filter_type):
        self._save_state()
        self._current = ImageProcessor.filter(self._current, filter_type)

class HistoryManager:
    """Управление историей (отдельно от логики изображений)"""
    def __init__(self, max_size=20):
        self._stack = []
        self._index = -1
        self._max = max_size
    
    def push(self, state):
        self._stack = self._stack[:self._index + 1]
        self._stack.append(state)
        self._index += 1
```
Фабричный метод для фильтров
```python
class ImageProcessor:
    @staticmethod
    def filter(image, filter_type):
        methods = {
            "bw": lambda img: img.convert("L").convert("RGBA"),
            "sepia": lambda img: ImageProcessor._sepia(img),
            "contrast": lambda img: ImageEnhance.Contrast(img).enhance(1.5),
        }
        return methods.get(filter_type, lambda x: x)(image)
```
Композиция эффектов текста
```python
class TextRenderer:
    @staticmethod
    def render(image, text, config):
        layers = []
        if config.get("shadow"):
            layers.append(TextRenderer._shadow_layer(text, config))
        layers.append(TextRenderer._outline_layer(text, config))
        layers.append(TextRenderer._main_layer(text, config))
        return Image.alpha_composite(image, Image.alpha_composite(*layers))
```