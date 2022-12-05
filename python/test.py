import tkinter as tk
import random

def make_segment():
    return [random.randrange(0, 800) for _ in range(4)]

def draw_random_lines():
    canvas.create_line(*make_segment())
    root.after(100, draw_random_lines)

root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=800)
canvas.pack()

draw_random_lines()

root.mainloop()