import tkinter as tk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("MarkEase - Watermark Images With Ease")
        self.root.resizable(False, False)
        self.root.configure(borderwidth=5)
        self.background()
        self.get_logo()
        self.root.mainloop()

    def get_logo(self):
        self.icon = ImageTk.PhotoImage(file="./Mark.png")
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)


    def background(self):
        bg = tk.Canvas(self.root)
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.update_idletasks()
        for y in range(720):
            r = 30 + int((y / 1280) * 50)
            g = 90 + int((y / 1280) * -75)
            b = 140 + int((y / 1280) * 25)
            color = f"#{r:02x}{g:02x}{b:02x}"
            bg.create_rectangle(1280, y, 0, y + 1, fill=color, outline="")