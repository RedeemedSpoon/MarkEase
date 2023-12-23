import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import webbrowser, os, tkcolorpicker

class MarkEase:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
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
        self.arrow_icon = ImageTk.PhotoImage(Image.open("./Images/arrow.png").resize((20, 20), Image.ADAPTIVE))

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
            self.canvas.create_rectangle(1280, y, 0, y + 1, fill=color, outline="", tags='background')
        
        self.image_on_canvas = None
        self.home_arrow_id = None
        self.home_text_id = None
        self.name = None
        self.buttons_list = []
        self.current_cursor = ""

        self.logo = ImageTk.PhotoImage(Image.open("./Images/Logo.png").resize((205, 53), Image.ADAPTIVE))
        self.logo_id = self.canvas.create_image(10, 10, anchor=tk.NW, image=self.logo, tags='brand')

        self.exit_id = self.canvas.create_text(1225, 680, text="Exit", anchor=tk.E, font=("Noto Sans", 12), fill="white", tags='side')
        self.exit_arrow_id = self.canvas.create_image(1255, 682, anchor=tk.E, image=self.arrow_icon, tags='side')
        self.canvas.tag_bind(self.exit_id, "<Button-1>", lambda event: quit())
        self.canvas.tag_bind(self.exit_id, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.exit_id, "<Leave>", lambda event: self.canvas.config(cursor=""))
        self.canvas.tag_bind(self.exit_arrow_id, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.exit_arrow_id, "<Leave>", lambda event: self.canvas.config(cursor=""))
        
        self.credit = self.canvas.create_text(125, 690, anchor="center", tags='link')
        self.canvas.itemconfig(self.credit, text="Created by RedeemedSpoon. Visit Repo", fill="white", font=("Noto Sans", 9, 'underline'))
        self.canvas.tag_bind(self.credit, "<Button-1>", self.open_link)
        self.canvas.tag_bind(self.credit, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.credit, "<Leave>", lambda event: self.canvas.config(cursor=""))
        
        self.options = {"JPEG Files": "*.jpg","PNG Files": "*.png","GIF Files": "*.gif","All Files": "*.*"}
        self.font_sizes = ["6", "8", "10", "12", "14", "16", "18"]
        self.watermark_width = ["X-Small", "Small", "Medium", "Big"]
        self.items_to_delete = [item for item in self.canvas.find_all() if all(tag not in self.canvas.gettags(item) for tag in ["background", "brand", "link", "side"])]

    def startup(self):
        self.root.title("MarkEase - Home")
        self.canvas.itemconfig(self.name, text="")
        self.canvas.delete(self.image_on_canvas)
        self.canvas.delete(self.home_arrow_id)
        self.canvas.delete(self.home_text_id)

        for item in self.items_to_delete:
            self.canvas.delete(item)
        for button in self.buttons_list:
            button.destroy()
            
        self.buttons_list.clear()
        self.opacity = 100
        self.color = "#000000"
        self.is_setup_screen = True
        
        self.slogan = self.canvas.create_text(640, 300, anchor="center")
        self.canvas.itemconfig(self.slogan, text="MarkEase - Watermark Images With Ease", fill="white", font=("Noto Sans", 40, "bold"))
            
        self.open = ttk.Button(self.canvas, text=" Import An Image", compound=tk.LEFT, image=self.upload_icon, command=self.import_image, style="TButton")
        self.open_id = self.canvas.create_window(620, 400, anchor=tk.CENTER, window=self.open)
        self.open.bind("<Enter>", lambda event, cursor="hand2": self.canvas.config(cursor=cursor))
        self.open.bind("<Leave>", lambda event: self.canvas.config(cursor=""))

    def start_edit(self):
        self.canvas.delete(self.slogan)      
        self.canvas.delete(self.home_arrow_id)
        self.canvas.delete(self.home_text_id)
        self.open.destroy()
        
        self.image_on_canvas = self.canvas.create_image((700, 337.5), anchor=tk.CENTER, image=self.photo)
        self.file_name = os.path.basename(self.file_path)
        self.root.title(f"MarkEase - {self.file_name}")
        self.name = self.canvas.create_text(700, 75, text=self.file_name, fill="white", font=("Noto Sans", 20, "bold"))
        
        self.home_arrow_id = self.canvas.create_image(1255, 25, anchor=tk.E, image=self.arrow_icon, tags='side')
        self.home_text_id = self.canvas.create_text(1180, 22.5, text="Home", anchor=tk.W, font=("Noto Sans", 12), fill="white", tags='side')
        self.canvas.tag_bind(self.home_text_id, "<Button-1>", lambda event: self.startup())
        self.canvas.tag_bind(self.home_text_id, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.home_text_id, "<Leave>", lambda event: self.canvas.config(cursor=""))
        self.canvas.tag_bind(self.home_arrow_id, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.home_arrow_id, "<Leave>", lambda event: self.canvas.config(cursor=""))
        
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
        
        for i, (button_info, x, y) in enumerate(zip(button_data, x_position, y_position)):
            button_widget = ttk.Button(self.canvas, **button_info)
            button_widget.place(x=x, y=y)
            self.buttons_list.append(button_widget)

            if button_info['command'] in [self.text, self.shape, self.watermark]:
                button_widget.bind("<Enter>", lambda event, cursor="hand2": self.canvas.config(cursor=cursor))
                button_widget.bind("<Leave>", lambda event: self.canvas.config(cursor=self.current_cursor))
                button_widget.bind("<Button-1>", lambda event, cursor="crosshair": self.set_cursor(cursor))
            else:
                button_widget.bind("<Enter>", lambda event, cursor="hand2": self.canvas.config(cursor=cursor))
                button_widget.bind("<Leave>", lambda event: self.canvas.config(cursor=self.current_cursor))
                button_widget.bind("<Button-1>", lambda event, cursor="": self.set_cursor(cursor))
                
    def set_cursor(self, cursor_type):
        self.current_cursor = cursor_type
        self.canvas.config(cursor=cursor_type)
            
    def open_link(self, event):
        webbrowser.open("https://www.youtube.com/watch?v=XlYsRxgWxNo")

    def import_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=list(self.options.items()), initialdir='~/', title="Select an image")
        if self.file_path:
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
                self.copy = self.photo
                self.canvas.itemconfig(self.name, text="")
                self.start_edit()
            except UnidentifiedImageError:
                messagebox.showerror(title='Error!', message="Error, Not a valid image!")

    def export_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=list(self.options.items()))
        if save_path:
            self.image.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")

    def text(self, finish=False):
        if finish:
            self.user_text = self.text_entry.get() 
            self.font_size = self.font_size_combobox.get()
            self.text_window.destroy()
            # Your Code Goes Here
        else:
            self.text_window = tk.Toplevel()
            self.text_window.title("Text Settings")
            self.text_window.geometry("400x200")
            self.text_window.resizable(False, False)

            ttk.Label(self.text_window, text="Enter Text:").grid(row=0, column=0, padx=10, pady=20)
            self.text_entry = ttk.Entry(self.text_window, width=20)
            self.text_entry.grid(row=0, column=1, padx=10, pady=20)

            ttk.Label(self.text_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=10)
            self.font_size_combobox = ttk.Combobox(self.text_window, values=self.font_sizes, width=15)
            self.font_size_combobox.set("10")
            self.font_size_combobox.grid(row=1, column=1, padx=10, pady=10)
            
            ttk.Button(self.text_window, text="OK", command=lambda: self.text(True)).grid(row=2, column=0, padx=30, pady=30)
            ttk.Button(self.text_window, text="Cancel", command=self.text_window.destroy).grid(row=2, column=1, padx=30, pady=30)
        
    def shape(self, finish=False):
        if finish:
            self.user_shape = self.shape_var.get()
            self.user_fill = self.fill_var.get()
            self.text_window.destroy()
            #Your Code Goes Here
        else:
            self.text_window = tk.Toplevel()
            self.text_window.title("Shape & Fill Settings")
            self.text_window.geometry("500x225")
            self.text_window.resizable(False, False)

            ttk.Label(self.text_window, text="Select Shape:").grid(row=0, column=0, padx=10, pady=20)
            self.shape_var = tk.StringVar(value="Rectangle")
            ttk.Radiobutton(self.text_window, text="Rectangle", variable=self.shape_var, value="Rectangle").grid(row=0, column=1, padx=10, pady=10)
            ttk.Radiobutton(self.text_window, text="Circle", variable=self.shape_var, value="Circle").grid(row=0, column=2, padx=10, pady=10)

            ttk.Label(self.text_window, text="Select Fill:").grid(row=1, column=0, padx=10, pady=10)
            self.fill_var = tk.StringVar(value="Fill")
            ttk.Radiobutton(self.text_window, text="Fill", variable=self.fill_var, value="Fill").grid(row=1, column=1, padx=10, pady=10)
            ttk.Radiobutton(self.text_window, text="No Fill", variable=self.fill_var, value="No Fill").grid(row=1, column=2, padx=10, pady=10)

            ttk.Button(self.text_window, text="OK", command=lambda: self.shape(True)).grid(row=2, column=2, padx=30, pady=30)
            ttk.Button(self.text_window, text="Cancel", command=self.text_window.destroy).grid(row=2, column=1, padx=30, pady=30)
        
    def watermark(self, finish=False):
        if finish:
            self.watermark_resoltion = self.image_resolution.get()
            self.watermark_window.destroy()
            #Your Code Goes Here
        else:
            self.file_path = filedialog.askopenfilename(filetypes=list(self.options.items()), initialdir='~/', title="Select an image")
            if self.file_path:
                try: 
                    self.watermark_img = Image.open(self.file_path)
                except UnidentifiedImageError:
                    messagebox.showerror(title='Error!', message="Error, Not a valid image!")
                else:
                    self.watermark_window = tk.Toplevel()
                    self.watermark_window.title("Watermark Settings")
                    self.watermark_window.geometry("300x200")
                    self.watermark_window.resizable(False, False)

                    ttk.Label(self.watermark_window, text="How big is the watermark?", font=("Noto Sans", 15)).pack(pady=10)
                    self.image_resolution = ttk.Combobox(self.watermark_window, values=self.watermark_width, width=10)
                    self.image_resolution.set("Small")
                    self.image_resolution.pack(pady=10)
                    
                    ttk.Button(self.watermark_window, text="OK", command=lambda: self.watermark(True)).pack(pady=20)

    
    def opacity_layer(self, finish=False):
        if finish:
            self.opacity = self.slider.get()
            self.opacity_window.destroy()
        else:
            self.opacity_window = tk.Toplevel(self.root)
            self.opacity_window.title("Opacity Settings")
            self.opacity_window.geometry("350x175")
            self.opacity_window.resizable(False, False)
            self.opacity_window.iconphoto(False, self.icon)

            label = tk.Label(self.opacity_window, text="Please select the level of opacity you want", font=("Noto Sans", 12))
            label.pack(pady=10)
            
            self.slider = tk.Scale(self.opacity_window, from_=0, to=100, orient="horizontal", length=200)
            self.slider.set(self.opacity)
            self.slider.pack(padx=20)

            ok_button = ttk.Button(self.opacity_window, text="Select", command=lambda: self.opacity_layer(True))
            ok_button.pack(side=tk.LEFT, padx=10, pady=10)
            cancel_button = ttk.Button(self.opacity_window, text="Cancel", command=self.opacity_window.destroy)
            cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def colorize(self):
        selected_color = tkcolorpicker.askcolor(title="Color Settings", color=self.color)[1]
        self.color = selected_color if selected_color else self.color

    def undo(self):
        self.image = self.copy
        self.opacity = 100
        self.color = '#000000'

if __name__ == '__main__':
    root = MarkEase()