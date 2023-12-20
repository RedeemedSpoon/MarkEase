import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import webbrowser

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("MarkEase - Watermark Images With Ease")
        self.root.resizable(False, False)
        self.root.configure(borderwidth=5)
        self.icon = ImageTk.PhotoImage(Image.open('./Images/Mark.png'))
        self.root.iconphoto(False, self.icon)
        self.style()
        self.buttons()
        self.initialize()
        self.startup()
        self.root.mainloop()
        
    def buttons(self):
        self.download_icon = ImageTk.PhotoImage(Image.open("./Images/download.png").resize((20, 20), Image.ADAPTIVE))
        self.upload_icon = ImageTk.PhotoImage(Image.open("./Images/upload.png").resize((20, 20), Image.ADAPTIVE))
        self.undo_icon = ImageTk.PhotoImage(Image.open("./Images/undo.png").resize((30, 30), Image.ADAPTIVE))
        self.image_icon = ImageTk.PhotoImage(Image.open("./Images/image.png").resize((30, 30), Image.ADAPTIVE))
        self.change_icon = ImageTk.PhotoImage(Image.open("./Images/change.png").resize((30, 30), Image.ADAPTIVE))
        self.text_icon = ImageTk.PhotoImage(Image.open("./Images/text.png").resize((30, 30), Image.ADAPTIVE))
        self.shape_icon = ImageTk.PhotoImage(Image.open("./Images/shapes.png").resize((30, 30), Image.ADAPTIVE))
        self.opacity_icon = ImageTk.PhotoImage(Image.open("./Images/opacity.png").resize((30, 30), Image.ADAPTIVE))

    def style(self):
        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 10, 10, 10), relief="flat", background="#309714", foreground="white", highlightthickness=0, font=("Droid Sans", 16, "bold"))
        self.style.map("TButton", background=[("active", "#266814")], relief=[("active", "flat")])
        
    def initialize(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0)
        self.canvas = tk.Canvas(frame, width=1267, height=708)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for y in range(720):
            r = 40 + int((y / 1280) * 70)
            g = 70 + int((y / 1280) * -110)
            b = 140 + int((y / 1280) * 50)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(1280, y, 0, y + 1, fill=color, outline="")
            
        self.logo = ImageTk.PhotoImage(Image.open("./Images/Logo.png").resize((205, 53), Image.ADAPTIVE))
        self.logo_id = self.canvas.create_image(10, 10, anchor=tk.NW, image=self.logo)
              
        self.open = ttk.Button(self.canvas, text=" Import An Image", compound=tk.LEFT, image=self.upload_icon, command=self.import_image, style="TButton")
        self.open_id = self.canvas.create_window(620, 400, anchor=tk.CENTER, window=self.open)
     
    def open_link(self, event):
        webbrowser.open("https://www.youtube.com/watch?v=XlYsRxgWxNo")
        
    def startup(self):
        self.slogan = self.canvas.create_text(640, 275, anchor="center")
        self.canvas.itemconfig(self.slogan, text="MarkEase - Watermark Images With Ease", fill="white", font=("Noto Sans", 30, "bold"))
        self.credit = self.canvas.create_text(125, 690, anchor="center")
        self.canvas.itemconfig(self.credit, text="Created by RedeemedSpoon. Visit Repo", fill="white", font=("Noto Sans", 9, 'underline'))
        self.canvas.tag_bind(self.credit, "<Button-1>", self.open_link)        
    
    def import_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("JPEG Files", "*.jpg"),("PNG Files", "*.png"),("GIF Files", "*.gif"),("All Files", "*.*")], initialdir='~/', title="Select an image")
        if self.file_path:
            self.image = Image.open(self.file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.edit()
    
    def edit(self):
        self.canvas.delete(self.slogan)
        self.open.destroy()
        
        self.save = ttk.Button(self.canvas, text="Export", compound=tk.LEFT, image=self.download_icon, command=self.import_image, style="TButton")
        self.save_id = self.canvas.create_window(900, 600, anchor=tk.CENTER, window=self.save)
        
        self.open = ttk.Button(self.canvas, text="Choose Another",compound=tk.LEFT, image=self.change_icon, command=self.import_image, style="TButton")
        self.open_id = self.canvas.create_window(600, 600, anchor=tk.CENTER, window=self.open)
        
        self.undo = ttk.Button(self.canvas, image=self.undo_icon, command=self.import_image, style="TButton")
        self.undo_id = self.canvas.create_window(200, 150, anchor=tk.CENTER, window=self.undo)
        
        self.mark = ttk.Button(self.canvas, image=self.image_icon, command=self.import_image, style="TButton")
        self.mark_id = self.canvas.create_window(200, 225, anchor=tk.CENTER, window=self.mark)
        
        self.text = ttk.Button(self.canvas, image=self.text_icon, command=self.import_image, style="TButton")
        self.text_id = self.canvas.create_window(200, 300, anchor=tk.CENTER, window=self.text)

        self.shape = ttk.Button(self.canvas, image=self.shape_icon, command=self.import_image, style="TButton")
        self.shape_id = self.canvas.create_window(200, 375, anchor=tk.CENTER, window=self.shape)

        self.opacity = ttk.Button(self.canvas, image=self.opacity_icon, command=self.import_image, style="TButton")
        self.opacity_id = self.canvas.create_window(200, 450, anchor=tk.CENTER, window=self.opacity)

if __name__ == '__main__':
    root = MainWindow()
