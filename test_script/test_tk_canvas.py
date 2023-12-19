import tkinter as tk
from PIL import Image, ImageTk

def draw_rectangle():
    # Coordinates of the rectangle (x1, y1, x2, y2)
    canvas.create_rectangle(50, 50, 150, 150, outline="red")

root = tk.Tk()
# self.root = root
root.title("Draw Rectangle on Image")

# Load the image


# Create a Canvas
image = Image.open("images/1.jpg")
photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()


root.mainloop()