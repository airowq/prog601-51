import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class SimpleMemeMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator")
        self.root.geometry("900x700")
        
        self.img_path = None
        self.img_orig = None
        self.photo = None  # для хранения ссылки на фото
        
        self.top_txt = tk.StringVar(value="ВЕРХНИЙ ТЕКСТ")
        self.bot_txt = tk.StringVar(value="НИЖНИЙ ТЕКСТ")
        self.font_sz = tk.IntVar(value=40)
        self.txt_clr = "#FFFFFF"
        self.out_clr = "#000000"
        
        self._build_ui()
    
    def _build_ui(self):
        # Используем ttk.Frame вместо tk.Frame (у ttk есть padding)
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)
        
        left = ttk.LabelFrame(main, text="Управление", padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(left, text="📁 Открыть", command=self._load).pack(fill=tk.X, pady=2)
        
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        ttk.Label(left, text="Верхний текст:").pack(anchor=tk.W)
        ttk.Entry(left, textvariable=self.top_txt, width=25).pack(pady=2)
        
        ttk.Label(left, text="Нижний текст:").pack(anchor=tk.W)
        ttk.Entry(left, textvariable=self.bot_txt, width=25).pack(pady=2)
        
        ttk.Label(left, text="Размер шрифта:").pack(anchor=tk.W)
        ttk.Spinbox(left, from_=10, to=120, textvariable=self.font_sz, width=23).pack(pady=2)
        
        # Цвет текста
        btn_frame1 = ttk.Frame(left)
        btn_frame1.pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame1, text="🎨 Цвет текста", command=self._pick_txt_clr).pack(side=tk.LEFT)
        self.txt_swatch = tk.Label(btn_frame1, text="    ", bg=self.txt_clr, relief=tk.RIDGE)
        self.txt_swatch.pack(side=tk.LEFT, padx=5)
        
        # Цвет обводки
        btn_frame2 = ttk.Frame(left)
        btn_frame2.pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame2, text="✒️ Цвет обводки", command=self._pick_out_clr).pack(side=tk.LEFT)
        self.out_swatch = tk.Label(btn_frame2, text="    ", bg=self.out_clr, relief=tk.RIDGE)
        self.out_swatch.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        ttk.Button(left, text="👁️ Предпросмотр", command=self._preview).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="💾 Сохранить", command=self._save).pack(fill=tk.X, pady=2)
        
        # Правая область с канвасом
        right = ttk.LabelFrame(main, text="Предпросмотр", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas = tk.Canvas(right, width=500, height=400, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _load(self):
        path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.img_path = path
            self.img_orig = Image.open(path)
            self.status.set(f"Загружено: {os.path.basename(path)}")
            self._preview()
    
    def _pick_txt_clr(self):
        c = colorchooser.askcolor(title="Цвет текста", initialcolor=self.txt_clr)
        if c[1]:
            self.txt_clr = c[1]
            self.txt_swatch.config(bg=self.txt_clr)
            self._preview()
    
    def _pick_out_clr(self):
        c = colorchooser.askcolor(title="Цвет обводки", initialcolor=self.out_clr)
        if c[1]:
            self.out_clr = c[1]
            self.out_swatch.config(bg=self.out_clr)
            self._preview()
    
    def _draw_with_outline(self, draw, text, pos, font, text_color, outline_color):
        """Рисует текст с чёрной обводкой"""
        x, y = pos
        # Обводка (смещения на 1-2 пикселя)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        # Основной текст
        draw.text((x, y), text, font=font, fill=text_color)
    
    def _preview(self):
        if not self.img_orig:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        
        # Копируем оригинал
        preview_img = self.img_orig.copy()
        
        # Масштабируем под размер канваса
        max_w = 500
        max_h = 400
        ratio = min(max_w / preview_img.width, max_h / preview_img.height)
        new_size = (int(preview_img.width * ratio), int(preview_img.height * ratio))
        preview_img = preview_img.resize(new_size, Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(preview_img)
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype("arial.ttf", self.font_sz.get())
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", self.font_sz.get())
            except:
                font = ImageFont.load_default()
        
        # Верхний текст
        top = self.top_txt.get().upper()
        if top:
            bbox = draw.textbbox((0, 0), top, font=font)
            text_w = bbox[2] - bbox[0]
            x = (preview_img.width - text_w) // 2
            y = 10
            self._draw_with_outline(draw, top, (x, y), font, self.txt_clr, self.out_clr)
        
        # Нижний текст
        bottom = self.bot_txt.get().upper()
        if bottom:
            bbox = draw.textbbox((0, 0), bottom, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            x = (preview_img.width - text_w) // 2
            y = preview_img.height - text_h - 10
            self._draw_with_outline(draw, bottom, (x, y), font, self.txt_clr, self.out_clr)
        
        # Отображаем
        self.photo = ImageTk.PhotoImage(preview_img)
        self.canvas.delete("all")
        self.canvas.config(width=preview_img.width, height=preview_img.height)
        self.canvas.create_image(preview_img.width // 2, preview_img.height // 2, image=self.photo, anchor="center")
    
    def _save(self):
        if not self.img_orig:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        if path:
            # Создаём финальное изображение в оригинальном размере
            final_img = self.img_orig.copy()
            draw = ImageDraw.Draw(final_img)
            
            try:
                font = ImageFont.truetype("arial.ttf", self.font_sz.get())
            except:
                try:
                    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", self.font_sz.get())
                except:
                    font = ImageFont.load_default()
            
            # Верхний текст
            top = self.top_txt.get().upper()
            if top:
                bbox = draw.textbbox((0, 0), top, font=font)
                text_w = bbox[2] - bbox[0]
                x = (final_img.width - text_w) // 2
                y = 10
                self._draw_with_outline(draw, top, (x, y), font, self.txt_clr, self.out_clr)
            
            # Нижний текст
            bottom = self.bot_txt.get().upper()
            if bottom:
                bbox = draw.textbbox((0, 0), bottom, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                x = (final_img.width - text_w) // 2
                y = final_img.height - text_h - 10
                self._draw_with_outline(draw, bottom, (x, y), font, self.txt_clr, self.out_clr)
            
            # Сохраняем
            final_img.save(path)
            self.status.set(f"Сохранено: {os.path.basename(path)}")
            messagebox.showinfo("Успех", f"Мем сохранён!\n{os.path.basename(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMemeMaker(root)
    root.mainloop()