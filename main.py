import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser, os

class MarkEase:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("MarkEase - Home")
        self.root.resizable(False, False)
        self.root.configure(borderwidth=5)
        self.icon = ImageTk.PhotoImage(Image.open("./Images/Mark.png"))
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
        self.color_icon = ImageTk.PhotoImage(Image.open("./Images/paint-bucket.png").resize((30, 30), Image.ADAPTIVE))

    def style(self):
        self.style = ttk.Style()
        self.style.configure("TButton", padding=(10, 10, 10, 10), relief="flat", background="#158a20", foreground="white", highlightthickness=0, font=("Droid Sans", 16, "bold"))
        self.style.map("TButton", background=[("active", "#106e19")], relief=[("active", "flat")])
        self.style.configure("F.TButton", padding=(10, 10, 10, 10), relief="flat", background="#e59400")
        self.style.map("F.TButton", background=[("active", "#b27300")], relief=[("active", "flat")])
        self.style.configure("A.TButton", padding=(10, 10, 10, 10), relief="flat", background="#ad1714", foreground="white", highlightthickness=0, font=("Droid Sans", 16, "bold"))
        self.style.map("A.TButton", background=[("active", "#8a1210")], relief=[("active", "flat")])

    def initialize(self):
        self.frame = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.frame, width=1267, height=708)
        self.canvas.pack(); self.frame.pack()

        for y in range(720):
            r = 50 + int((y / 1280) * 40)
            g = 70 + int((y / 1280) * -120)
            b = 140 + int((y / 1280) * 60)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(1280, y, 0, y + 1, fill=color, outline="")

        self.logo = ImageTk.PhotoImage(Image.open("./Images/Logo.png").resize((205, 53), Image.ADAPTIVE))
        self.logo_id = self.canvas.create_image(10, 10, anchor=tk.NW, image=self.logo)
        self.open = ttk.Button(self.canvas, text=" Import An Image", compound=tk.LEFT, image=self.upload_icon, command=self.import_image, style="TButton")
        self.open_id = self.canvas.create_window(620, 400, anchor=tk.CENTER, window=self.open) 
        self.options = {"JPEG Files": "*.jpg","PNG Files": "*.png","GIF Files": "*.gif","All Files": "*.*"}

    def startup(self):
        self.slogan = self.canvas.create_text(640, 300, anchor="center")
        self.canvas.itemconfig(self.slogan, text="MarkEase - Watermark Images With Ease", fill="white", font=("Noto Sans", 40, "bold"))
        self.credit = self.canvas.create_text(125, 690, anchor="center")
        self.canvas.itemconfig(self.credit, text="Created by RedeemedSpoon. Visit Repo", fill="white", font=("Noto Sans", 9, 'underline'))
        self.name = self.canvas.create_text(700,75, text="", fill="white", font=("Noto Sans", 20, "bold"))
        
        self.canvas.tag_bind(self.credit, "<Button-1>", self.open_link)
        self.canvas.tag_bind(self.credit, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.credit, "<Leave>", lambda event: self.canvas.config(cursor=""))
        self.open.bind("<Enter>", lambda event, cursor="hand2": self.canvas.config(cursor=cursor))
        self.open.bind("<Leave>", lambda event: self.canvas.config(cursor=""))

    def open_link(self, event):
        webbrowser.open("https://www.youtube.com/watch?v=XlYsRxgWxNo")

    def import_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=list(self.options.items()), initialdir='~/', title="Select an image")
        try: 
            self.image = Image.open(self.file_path)
            aspect_ratio = 720 / 405
            width, height = self.image.size
            image_ratio = width / height
            if image_ratio > aspect_ratio:
                new_width = 720
                new_height = int(720 / 405)
            else:
                new_height = 405
                new_width = int(405 * image_ratio)
                
            self.image = self.image.resize((new_width, new_height), Image.ADAPTIVE)
            self.photo = ImageTk.PhotoImage(self.image)
            self.start_edit()
        except:
            messagebox.showerror(title='Error!', message="Error, Not a valid image!")

    def export_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=list(self.options.items()))
        if save_path:
            self.image.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")

    def text(self):
        pass

    def shape(self):
        pass
    
    def watermark(self):
        pass
                
    def opacity_layer(self):
        pass
    
    def colorize(self):
        pass

    def undo(self):
        pass

    def start_edit(self):
        self.canvas.delete(self.slogan)
        self.open.destroy()
        self.image_on_canvas = self.canvas.create_image((700, 337.5), anchor=tk.CENTER, image=self.photo)
        self.file_name = os.path.basename(self.file_path)
        self.root.title(f"MarkEase - {self.file_name}")
        self.canvas.itemconfigure(self.name, text=self.file_name)

        button_data = [
            {"text": "Export", "compound": tk.LEFT, "image": self.download_icon, "command": self.export_image, "style": "TButton"},
            {"text": "Choose Another", "compound": tk.LEFT, "image": self.change_icon, "command": self.import_image, "style": "A.TButton"},
            {"image": self.undo_icon, "command": self.undo, "style": "F.TButton"},
            {"image": self.image_icon, "command": self.watermark, "style": "F.TButton"},
            {"image": self.text_icon, "command": self.text, "style": "F.TButton"},
            {"image": self.shape_icon, "command": self.shape, "style": "F.TButton"},
            {"image": self.opacity_icon, "command": self.opacity_layer, "style": "F.TButton"},
            {"image": self.color_icon, "command": self.colorize, "style": "F.TButton"}
        ]

        x_position = [800, 400, 200, 200, 200, 200, 200, 200]
        y_position = [600, 600, 125, 200, 275, 350, 425, 500]
        self.buttons_list = []

        for i, (button_info, x, y) in enumerate(zip(button_data, x_position, y_position)):
            button_widget = ttk.Button(self.canvas, **button_info)
            button_widget.place(x=x, y=y)
            self.buttons_list.append(button_widget)

        for button in self.buttons_list:
            button.bind("<Enter>", lambda event, cursor="hand2": self.canvas.config(cursor=cursor))
            button.bind("<Leave>", lambda event: self.canvas.config(cursor=""))

if __name__ == '__main__':
    root = MarkEase()