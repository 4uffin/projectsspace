import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Configuration
CANVAS_SIZE = 400
CELL_SIZE = 20
COLS = CANVAS_SIZE // CELL_SIZE
ROWS = CANVAS_SIZE // CELL_SIZE
COLOR_PALETTE = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]

class PixelCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Canvas Game")

        self.current_mode = "color"
        self.current_color = "#000000"
        self.current_image = None
        self.show_grid = True

        self.cell_size = CELL_SIZE
        self.grid_data = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.cell_images = {}
        self.color_swatch_images = {}
        self.preset_thumbnails = {}

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.root)
        container.pack(padx=20, pady=20)

        # Toolbar
        toolbar = tk.Frame(container)
        toolbar.pack(pady=(0, 10))

        self.brush_label = tk.Label(toolbar, text="Pixel: #000000")
        self.brush_label.pack(side=tk.LEFT, padx=(0, 10))

        # Pick Pixel Menu
        menu_button = tk.Menubutton(toolbar, text="Pick Pixel", relief=tk.RAISED)
        menu_button.pack(side=tk.LEFT)

        self.pick_pixel_menu = tk.Menu(menu_button, tearoff=0)
        menu_button.config(menu=self.pick_pixel_menu)

        # Colors submenu
        color_menu = tk.Menu(self.pick_pixel_menu, tearoff=0)
        self.pick_pixel_menu.add_cascade(label="Colors", menu=color_menu)
        for color in COLOR_PALETTE:
            swatch = tk.PhotoImage(width=16, height=16)
            swatch.put(color, to=(0, 0, 16, 16))
            self.color_swatch_images[color] = swatch
            color_menu.add_command(image=swatch, compound="left", command=lambda c=color: self.select_color(c))

        # Custom Images submenu
        custom_menu = tk.Menu(self.pick_pixel_menu, tearoff=0)
        self.pick_pixel_menu.add_cascade(label="Custom Images", menu=custom_menu)

        # Preset image URLs
        preset_paths = {
            "Grass": "https://duffin.neocities.org/images/pixelcanvas/minecraft_grass_block_by_flutterspon-d9hlkmq-4192425799.jpg",
            "Dirt": "https://duffin.neocities.org/images/pixelcanvas/2ab1c37cfdff720c6de2ddb07328f145-4195645521.jpg",
            "Stone": "https://duffin.neocities.org/images/pixelcanvas/eqpOX-1763668591.png",
            "Cobblestone": "https://duffin.neocities.org/images/pixelcanvas/minecraft%20texturas%20classicas%20-%209-2090894536.jpg",
            "Sand": "https://duffin.neocities.org/images/pixelcanvas/s189772745713394276_p3861_i148_w750-3664175598.jpeg",
            "Sandstone": "https://duffin.neocities.org/images/pixelcanvas/638152134000748859-903807525.png",
            "Water": "https://duffin.neocities.org/images/pixelcanvas/13327895-pack_m-1852891663.jpg",
            "Lava": "https://duffin.neocities.org/images/pixelcanvas/13914790-pack-icon_xl-2701408835.jpg",
        }

        for label, url in preset_paths.items():
            try:
                response = requests.get(url)
                response.raise_for_status()
                img_data = BytesIO(response.content)
                img = Image.open(img_data).resize((16, 16), Image.LANCZOS)
                thumb = ImageTk.PhotoImage(img)
                self.preset_thumbnails[label] = thumb
                custom_menu.add_command(
                    label=label,
                    image=thumb,
                    compound="left",
                    command=lambda u=url, l=label: self.load_preset_image(u, l)
                )
            except Exception as e:
                print(f"Failed to load preset image '{label}': {e}")
                custom_menu.add_command(label=label + " (Failed to Load)", state="disabled")

        custom_menu.add_separator()
        custom_menu.add_command(label="Load Custom Image...", command=self.load_image_brush)

        # Canvas
        self.canvas = tk.Canvas(container, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#ffffff", cursor="cross")
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind("<Key>", self.toggle_grid)

        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x = col * self.cell_size
                y = row * self.cell_size
                cell = self.grid_data[row][col]
                if cell:
                    if cell['mode'] == "color":
                        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                     fill=cell['val'], outline="")
                    elif cell['mode'] == "image":
                        img = cell['val']
                        self.cell_images[(row, col)] = img
                        self.canvas.create_image(x, y, anchor='nw', image=img)
        if self.show_grid:
            for x in range(0, CANVAS_SIZE + 1, self.cell_size):
                self.canvas.create_line(x, 0, x, CANVAS_SIZE, fill="#ddd")
            for y in range(0, CANVAS_SIZE + 1, self.cell_size):
                self.canvas.create_line(0, y, CANVAS_SIZE, y, fill="#ddd")

    def draw_at(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= col < COLS and 0 <= row < ROWS:
            if self.current_mode == "color":
                self.grid_data[row][col] = {'mode': 'color', 'val': self.current_color}
            elif self.current_mode == "image" and self.current_image:
                self.grid_data[row][col] = {'mode': 'image', 'val': self.current_image}
            self.redraw_canvas()

    def on_mouse_down(self, event):
        self.draw_at(event)
        self.canvas.bind("<B1-Motion>", self.draw_at)

    def on_mouse_up(self, event):
        self.canvas.unbind("<B1-Motion>")

    def toggle_grid(self, event):
        if event.char.lower() == 'g':
            self.show_grid = not self.show_grid
            self.redraw_canvas()

    def select_color(self, color):
        self.current_mode = "color"
        self.current_color = color
        self.brush_label.config(text=f"Pixel: {color}")

    def load_image_brush(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not file_path:
            return
        try:
            img = Image.open(file_path).resize((self.cell_size, self.cell_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.current_mode = "image"
            self.current_image = photo
            self.brush_label.config(text="Pixel: Custom Image")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image:\n{e}")

    def load_preset_image(self, url, label):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data).resize((self.cell_size, self.cell_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.current_mode = "image"
            self.current_image = photo
            self.brush_label.config(text=f"Pixel: {label}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load preset image:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelCanvas(root)
    root.mainloop()
