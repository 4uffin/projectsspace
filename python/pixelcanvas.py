import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # Requires Pillow: pip install Pillow

# Configuration
CANVAS_SIZE = 400
CELL_SIZE = 20
COLS = CANVAS_SIZE // CELL_SIZE
ROWS = CANVAS_SIZE // CELL_SIZE

# Global drawing state
current_mode = "color"       # Can be "color" or "image"
current_color = "#000000"    # default color
current_image = None         # will hold a PhotoImage when in image mode
show_grid = True

# We use a grid data structure to remember each cell's content.
# Each cell entry is either None or a dictionary with:
#   'mode': "color" or "image"
#   'val' : the color hex string OR the PhotoImage object.
grid_data = [[None for _ in range(COLS)] for _ in range(ROWS)]
# To keep references to PhotoImage objects (so they are not garbage-collected)
cell_images = {}

def redraw_canvas():
    """Clear and redraw all cells and grid lines on the canvas."""
    canvas.delete("all")
    # Draw cell contents
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            cell = grid_data[row][col]
            if cell is not None:
                if cell['mode'] == "color":
                    canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                            fill=cell['val'], outline="")
                elif cell['mode'] == "image":
                    # Draw image at cell location
                    # We assume the image is already a PhotoImage resized to (CELL_SIZE, CELL_SIZE)
                    img = cell['val']
                    # Keep a reference to avoid garbage-collection:
                    cell_images[(row, col)] = img
                    canvas.create_image(x, y, anchor='nw', image=img)
    # Draw grid lines on top if enabled
    if show_grid:
        for x in range(0, CANVAS_SIZE + 1, CELL_SIZE):
            canvas.create_line(x, 0, x, CANVAS_SIZE, fill="#ddd")
        for y in range(0, CANVAS_SIZE + 1, CELL_SIZE):
            canvas.create_line(0, y, CANVAS_SIZE, y, fill="#ddd")

def draw_at(event):
    """Compute the grid cell from (x,y) and update its contents."""
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        if current_mode == "color":
            grid_data[row][col] = {'mode': 'color', 'val': current_color}
        elif current_mode == "image" and current_image is not None:
            grid_data[row][col] = {'mode': 'image', 'val': current_image}
        redraw_canvas()

def on_mouse_down(event):
    draw_at(event)
    canvas.bind('<B1-Motion>', draw_at)

def on_mouse_up(event):
    canvas.unbind('<B1-Motion>')

def toggle_grid(event):
    global show_grid
    if event.char.lower() == 'g':
        show_grid = not show_grid
        redraw_canvas()

def select_color(color):
    global current_mode, current_color
    current_mode = "color"
    current_color = color
    brush_label.config(text=f"Brush: {color}")

def load_image_brush():
    global current_mode, current_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if not file_path:
        return
    try:
        # Open the image, resize to cell size, and convert to PhotoImage
        img = Image.open(file_path).resize((CELL_SIZE, CELL_SIZE), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        current_mode = "image"
        current_image = photo
        brush_label.config(text="Brush: Custom Image")
    except Exception as e:
        print("Error loading image:", e)

# Main application window
root = tk.Tk()
root.title("Pixel Canvas Game")

# Main container frame
container = tk.Frame(root)
container.pack(padx=20, pady=20)

# Toolbar frame at the top
toolbar = tk.Frame(container)
toolbar.pack(pady=(0,10))

# A label to show the current brush
brush_label = tk.Label(toolbar, text="Brush: #000000")
brush_label.pack(side=tk.LEFT, padx=(0, 10))

# Color palette (buttons with preset colors)
colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
for color in colors:
    btn = tk.Button(toolbar, bg=color, width=2, command=lambda c=color: select_color(c))
    btn.pack(side=tk.LEFT, padx=2)

# Button for loading a custom image as brush
img_brush_btn = tk.Button(toolbar, text="Load Image Brush", command=load_image_brush)
img_brush_btn.pack(side=tk.LEFT, padx=10)

# Create the canvas
canvas = tk.Canvas(container, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#ffffff", cursor="cross")
canvas.pack()

# Bind mouse and key events
canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
root.bind("<Key>", toggle_grid)

# Initial draw of the grid on the blank canvas
redraw_canvas()

root.mainloop()
