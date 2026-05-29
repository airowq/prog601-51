import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageEnhance
import os
from collections import deque

# ========== ОТДЕЛЬНЫЕ КОМПОНЕНТЫ ==========

class ImageState:
    """Хранилище состояния изображения"""
    def __init__(self):
        self.original = None
        self.current = None
    
    def load(self, path):
        self.original = Image.open(path)
        self.current = self.original.copy()
        return True
    
    def reset(self):
        if self.original:
            self.current = self.original.copy()
    
    def get_copy(self):
        return self.current.copy()

class HistoryKeeper:
    """Управление историей"""
    def __init__(self, limit=20):
        self._storage = deque(maxlen=limit)
        self._cursor = -1
    
    def push(self, state_image):
        self._storage.append(state_image.copy())
        self._cursor = len(self._storage) - 1
    
    def undo(self):
        if self._cursor > 0:
            self._cursor -= 1
            return self._storage[self._cursor].copy()
        return None
    
    def redo(self):
        if self._cursor < len(self._storage) - 1:
            self._cursor += 1
            return self._storage[self._cursor].copy()
        return None

class TextConfig:
    """Конфигурация текста"""
    def __init__(self):
        self.top = tk.StringVar(value="ВЕРХНИЙ ТЕКСТ")
        self.bottom = tk.StringVar(value="НИЖНИЙ ТЕКСТ")
        self.size = tk.IntVar(value=40)
        self.color = "#FFFFFF"
        self.outline = "#000000"
        self.shadow = tk.BooleanVar(value=False)
        self.opacity = tk.IntVar(value=100)
        self.rotation = tk.IntVar(value=0)
        self.position = tk.StringVar(value="center")
        self.custom_x = tk.IntVar(value=0)
        self.custom_y = tk.IntVar(value=0)
        self.font_path = "arial.ttf"

class ImageFilters:
    """Набор фильтров для изображений"""
    
    @staticmethod
    def black_white(img):
        return img.convert("L").convert("RGBA")
    
    @staticmethod
    def sepia(img):
        result = img.copy()
        pixels = result.load()
        for x in range(result.size[0]):
            for y in range(result.size[1]):
                r, g, b, a = pixels[x, y]
                tr = int(min(255, 0.393*r + 0.769*g + 0.189*b))
                tg = int(min(255, 0.349*r + 0.686*g + 0.168*b))
                tb = int(min(255, 0.272*r + 0.534*g + 0.131*b))
                pixels[x, y] = (tr, tg, tb, a)
        return result
    
    @staticmethod
    def contrast(img, factor=1.5):
        return ImageEnhance.Contrast(img).enhance(factor)
    
    @staticmethod
    def brightness(img, factor=1.3):
        return ImageEnhance.Brightness(img).enhance(factor)
    
    @staticmethod
    def darken(img, factor=0.5):
        return ImageEnhance.Brightness(img).enhance(factor)

class TextRenderer:
    """Отрисовщик текста на изображении"""
    
    @staticmethod
    def get_font(font_path, size):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            return ImageFont.load_default()
    
    @staticmethod
    def draw_with_effects(draw, text, pos, font, cfg, img_size):
        x, y = pos
        w, h = img_size
        
        layer = Image.new("RGBA", (w, h), (0,0,0,0))
        layer_draw = ImageDraw.Draw(layer)
        
        # Тень
        if cfg.shadow.get():
            for dx, dy in [(2,2), (1,2), (2,1)]:
                layer_draw.text((x+dx, y+dy), text, font=font, fill="#000000")
        
        # Обводка
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    layer_draw.text((x+dx, y+dy), text, font=font, fill=cfg.outline)
        
        # Основной текст
        layer_draw.text((x, y), text, font=font, fill=cfg.color)
        
        # Поворот
        if cfg.rotation.get() != 0:
            layer = layer.rotate(cfg.rotation.get(), expand=True, center=(x, y))
        
        # Прозрачность
        if cfg.opacity.get() < 100:
            alpha = int(255 * cfg.opacity.get() / 100)
            r,g,b,a = layer.split()
            a = a.point(lambda p: min(p, alpha))
            layer = Image.merge("RGBA", (r,g,b,a))
        
        draw._image.paste(layer, (0,0), layer)
    
    @staticmethod
    def calc_position(draw, text, font, img_w, img_h, is_top, cfg):
        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        pos_type = cfg.position.get()
        if pos_type == "center":
            x = (img_w - tw) // 2
        elif pos_type == "left":
            x = 10
        elif pos_type == "right":
            x = img_w - tw - 10
        else:
            x = cfg.custom_x.get()
        
        y = 10 if is_top else img_h - th - 10
        return (x, y)

# ========== ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ ==========

class MemeGeneratorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator Pro")
        self.root.geometry("1100x750")
        
        # Компоненты
        self.state = ImageState()
        self.history = HistoryKeeper()
        self.cfg = TextConfig()
        
        # GUI элементы
        self.image_tk = None
        self.canvas = None
        
        self._setup_gui()
        self._setup_menu()
        self._setup_hotkeys()
    
    def _setup_gui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._tab_main(notebook)
        self._tab_advanced(notebook)
        self._tab_filters(notebook)
        
        self.status = tk.StringVar(value="Готов")
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN).pack(side=tk.BOTTOM, fill=tk.X)
    
    def _tab_main(self, parent):
        tab = ttk.Frame(parent)
        parent.add(tab, text="Основные")
        
        left = ttk.LabelFrame(tab, text="Управление", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(left, text="Загрузить", command=self._load, width=25).pack(pady=5)
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(left, text="Верхний текст:").pack(anchor=tk.W)
        ttk.Entry(left, textvariable=self.cfg.top, width=30).pack(pady=2)
        ttk.Label(left, text="Нижний текст:").pack(anchor=tk.W)
        ttk.Entry(left, textvariable=self.cfg.bottom, width=30).pack(pady=2)
        
        ttk.Label(left, text="Размер:").pack(anchor=tk.W)
        ttk.Scale(left, from_=10, to=120, variable=self.cfg.size, command=lambda x: self._preview()).pack(fill=tk.X)
        
        cf = ttk.Frame(left)
        cf.pack(fill=tk.X, pady=5)
        ttk.Button(cf, text="Цвет текста", command=self._pick_text_color).pack(side=tk.LEFT)
        self.color_swatch = tk.Label(cf, text="    ", bg=self.cfg.color, relief=tk.RIDGE)
        self.color_swatch.pack(side=tk.LEFT, padx=2)
        ttk.Button(cf, text="Цвет обводки", command=self._pick_outline_color).pack(side=tk.LEFT)
        self.outline_swatch = tk.Label(cf, text="    ", bg=self.cfg.outline, relief=tk.RIDGE)
        self.outline_swatch.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        btnf = ttk.Frame(left)
        btnf.pack(fill=tk.X)
        ttk.Button(btnf, text="Предпросмотр", command=self._preview).pack(side=tk.LEFT, padx=2)
        ttk.Button(btnf, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=2)
        
        right = ttk.LabelFrame(tab, text="Предпросмотр", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(right, width=550, height=450, bg="#2b2b2b")
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def _tab_advanced(self, parent):
        tab = ttk.Frame(parent)
        parent.add(tab, text="Расширенные")
        
        f1 = ttk.LabelFrame(tab, text="Шрифт", padding=10)
        f1.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(f1, text="Загрузить шрифт", command=self._load_font).pack()
        
        f2 = ttk.LabelFrame(tab, text="Эффекты", padding=10)
        f2.pack(fill=tk.X, padx=10, pady=5)
        ttk.Checkbutton(f2, text="Тень", variable=self.cfg.shadow, command=self._preview).pack(anchor=tk.W)
        ttk.Label(f2, text="Прозрачность:").pack(anchor=tk.W)
        ttk.Scale(f2, from_=0, to=100, variable=self.cfg.opacity, command=lambda x: self._preview()).pack(fill=tk.X)
        ttk.Label(f2, text="Поворот:").pack(anchor=tk.W)
        ttk.Scale(f2, from_=-180, to=180, variable=self.cfg.rotation, command=lambda x: self._preview()).pack(fill=tk.X)
        
        f3 = ttk.LabelFrame(tab, text="Позиция", padding=10)
        f3.pack(fill=tk.X, padx=10, pady=5)
        for label, val in [("Центр","center"), ("Лево","left"), ("Право","right"), ("Вручную","custom")]:
            ttk.Radiobutton(f3, text=label, variable=self.cfg.position, value=val, command=self._preview).pack(anchor=tk.W)
        
        cf = ttk.Frame(f3)
        cf.pack(fill=tk.X, pady=5)
        ttk.Label(cf, text="X:").pack(side=tk.LEFT)
        ttk.Spinbox(cf, from_=0, to=1000, textvariable=self.cfg.custom_x, width=5, command=self._preview).pack(side=tk.LEFT)
        ttk.Label(cf, text="Y:").pack(side=tk.LEFT)
        ttk.Spinbox(cf, from_=0, to=1000, textvariable=self.cfg.custom_y, width=5, command=self._preview).pack(side=tk.LEFT)
    
    def _tab_filters(self, parent):
        tab = ttk.Frame(parent)
        parent.add(tab, text="Фильтры")
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        filters = [
            ("Оригинал", self._reset),
            ("Ч/Б", lambda: self._apply_filter("bw")),
            ("Сепия", lambda: self._apply_filter("sepia")),
            ("Контраст+", lambda: self._apply_filter("contrast")),
            ("Яркость+", lambda: self._apply_filter("bright")),
            ("Затемнить", lambda: self._apply_filter("dark")),
        ]
        for i, (name, cmd) in enumerate(filters):
            ttk.Button(frame, text=name, command=cmd, width=20).grid(row=i//3, column=i%3, padx=5, pady=5)
    
    def _setup_menu(self):
        mb = tk.Menu(self.root)
        self.root.config(menu=mb)
        
        fm = tk.Menu(mb, tearoff=0)
        mb.add_cascade(label="Файл", menu=fm)
        fm.add_command(label="Открыть", command=self._load, accelerator="Ctrl+O")
        fm.add_command(label="Сохранить", command=self._save, accelerator="Ctrl+S")
        fm.add_separator()
        fm.add_command(label="Выход", command=self.root.quit)
        
        em = tk.Menu(mb, tearoff=0)
        mb.add_cascade(label="Правка", menu=em)
        em.add_command(label="Отменить", command=self._undo, accelerator="Ctrl+Z")
        em.add_command(label="Повторить", command=self._redo, accelerator="Ctrl+Y")
    
    def _setup_hotkeys(self):
        self.root.bind("<Control-o>", lambda e: self._load())
        self.root.bind("<Control-s>", lambda e: self._save())
        self.root.bind("<Control-z>", lambda e: self._undo())
        self.root.bind("<Control-y>", lambda e: self._redo())
    
    def _load(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.state.load(path)
            self.history.push(self.state.current)
            self.status.set(f"Загружено: {os.path.basename(path)}")
            self._preview()
    
    def _load_font(self):
        path = filedialog.askopenfilename(filetypes=[("TTF", "*.ttf")])
        if path:
            self.cfg.font_path = path
            self.status.set(f"Шрифт: {os.path.basename(path)}")
            self._preview()
    
    def _pick_text_color(self):
        c = colorchooser.askcolor(initialcolor=self.cfg.color)
        if c[1]:
            self.cfg.color = c[1]
            self.color_swatch.config(bg=self.cfg.color)
            self._preview()
    
    def _pick_outline_color(self):
        c = colorchooser.askcolor(initialcolor=self.cfg.outline)
        if c[1]:
            self.cfg.outline = c[1]
            self.outline_swatch.config(bg=self.cfg.outline)
            self._preview()
    
    def _apply_filter(self, ftype):
        if not self.state.current:
            return
        self.history.push(self.state.current)
        filters = {
            "bw": ImageFilters.black_white,
            "sepia": ImageFilters.sepia,
            "contrast": lambda i: ImageFilters.contrast(i, 1.5),
            "bright": lambda i: ImageFilters.brightness(i, 1.3),
            "dark": lambda i: ImageFilters.darken(i, 0.5),
        }
        self.state.current = filters.get(ftype, lambda x: x)(self.state.current)
        self.status.set(f"Фильтр: {ftype}")
        self._preview()
    
    def _reset(self):
        if self.state.original:
            self.history.push(self.state.current)
            self.state.reset()
            self.status.set("Сброшено")
            self._preview()
    
    def _undo(self):
        restored = self.history.undo()
        if restored:
            self.state.current = restored
            self._preview()
            self.status.set("Отмена")
    
    def _redo(self):
        restored = self.history.redo()
        if restored:
            self.state.current = restored
            self._preview()
            self.status.set("Повтор")
    
    def _preview(self):
        if not self.state.current:
            messagebox.showwarning("Ошибка", "Загрузите изображение")
            return
        
        img = self.state.current.copy()
        max_w, max_h = 550, 450
        ratio = min(max_w/img.width, max_h/img.height)
        newsize = (int(img.width*ratio), int(img.height*ratio))
        img = img.resize(newsize, Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        font = TextRenderer.get_font(self.cfg.font_path, self.cfg.size.get())
        
        for text, is_top in [(self.cfg.top.get().upper(), True), (self.cfg.bottom.get().upper(), False)]:
            if text:
                pos = TextRenderer.calc_position(draw, text, font, img.width, img.height, is_top, self.cfg)
                TextRenderer.draw_with_effects(draw, text, pos, font, self.cfg, (img.width, img.height))
        
        self.image_tk = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.config(width=img.width, height=img.height)
        self.canvas.create_image(img.width//2, img.height//2, image=self.image_tk, anchor="center")
    
    def _save(self):
        if not self.state.current:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
        if path:
            img = self.state.current.copy()
            draw = ImageDraw.Draw(img)
            font = TextRenderer.get_font(self.cfg.font_path, self.cfg.size.get())
            for text, is_top in [(self.cfg.top.get().upper(), True), (self.cfg.bottom.get().upper(), False)]:
                if text:
                    pos = TextRenderer.calc_position(draw, text, font, img.width, img.height, is_top, self.cfg)
                    TextRenderer.draw_with_effects(draw, text, pos, font, self.cfg, (img.width, img.height))
            img.save(path)
            self.status.set(f"Сохранено: {os.path.basename(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGeneratorPro(root)
    root.mainloop()