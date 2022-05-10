from tkinter import Label, Tk, Text, font, simpledialog, filedialog
import tkinter
from tkinter.constants import END
from PIL import Image, ImageTk, ImageFont, ImageDraw
from os import remove, system
import subprocess


class Widgets:

    def close_button(self, root, width=263, height=187):

        close_bg = ImageTk.PhotoImage(Image.open("close.png"))
        close_clk = ImageTk.PhotoImage(Image.open("closeActive.png"))

        close = Label(image=close_bg)
        close.place(x=width * 0.9, y=height * 0.037,
                    width=width * 0.068, height=height * 0.096)
        close.image = close_bg
        close.bind("<ButtonRelease>", lambda x: self.Return(root))
        close.bind("<Enter>", lambda x: self.change_image(close, close_clk))
        close.bind("<Leave>", lambda x: self.change_image(close, close_bg))

        return close

    def add_buttons(self, root, image, X, Y, command):
        button_bg = ImageTk.PhotoImage(Image.open(image))
        yes_active = ImageTk.PhotoImage(Image.open(
            str(image[:-(len(".png"))] + "Active" + ".png")))
        button = Label(root, image=button_bg,
                       relief="sunken", borderwidth=0)
        button.image = button_bg
        button.place(x=X, y=Y)
        button.bind("<ButtonPress-1>",
                    lambda x: self.change_image(button, button_bg))
        button.bind("<ButtonRelease-1>", command)
        button.bind("<Enter>", lambda x: self.change_image(button, yes_active))
        button.bind("<Leave>", lambda x: self.change_image(button, button_bg))

    # def add_label(self, root, X, Y):

    #     _bg = Image.open("entrybg.png")
    #     bg = ImageTk.PhotoImage(_bg)
    #     entry_bg = Label(root, image=bg)
    #     W, H = _bg.size
    #     entry_bg.place(x=X, y=Y, width=W, height=H)
    #     entry_bg.image = bg

    #     entry = Label(root)  # Entry(root)
    #     entry["borderwidth"] = "1px"
    #     entry["justify"] = "left"
    #     entry.configure(relief='flat', background="#ffffff")
    #     entry.place(x=X + (W * 0.1), y=Y + (H * 0.1),
    #                 width=W * 0.75, height=H * 0.8)

    #     return entry

    def add_entry(self, root, X, Y):

        ft = font.Font(family='Montserrat', size=8)
        _bg = Image.open("entrybg.png")
        bg = ImageTk.PhotoImage(_bg)
        entry_bg = Label(root, image=bg)
        W, H = _bg.size
        entry_bg.place(x=X, y=Y, width=W, height=H)
        entry_bg.image = bg

        entry = Text(root)  # Entry(root)
        entry["borderwidth"] = "1px"
        entry.configure(relief='flat', background="#ffffff", font=ft)
        entry.place(x=X + (W * 0.1), y=Y + (H * 0.1),
                    width=W * 0.75, height=H * 0.8)

        return entry

    def Return(self, root, isconfirm: bool = False):
        self.is_confirm = isconfirm
        self.clear_cache()
        root.destroy()

    def change_image(self, widget, image):
        widget.configure(image=image)

    def clear_cache(self):
        try:
            for x in self._CACHE_LIST:
                remove(str(x))
        except:
            print("<CacheError>:Unable to clear or find cached files")


class App(Widgets):

    _CACHE_LIST = []

    def __init__(self, root, image="menuscreen.png"):

        self.FOLDER_NAME, self.PATH = "", ""

        image_ = Image.open(image)
        width, height = image_.size
        root.geometry(f"{width}x{height}")
        self.box(root)

        self.TEXT = self.add_entry(
            root, width * 0.38, height * 0.25)

        self.close_button(root, width + 20, height - 20)
        self.add_buttons(root, "environment.png", width * 0.1,
                         height * 0.45, lambda *args: self._action("<Environment>"))
        self.add_buttons(root, "project.png", width * 0.4025,
                         height * 0.45, lambda *args: self._action("<Project>"))
        self.add_buttons(
            root, "app.png", width * 0.7, height * 0.45, lambda *args: self._action("<App>"))

        root.attributes("-topmost", True)
        root.mainloop()

    def _action(self, type: str):
        self.FOLDER_NAME = (self.TEXT.get(1.0, END)).strip('\n')
        if self.FOLDER_NAME:
            self.PATH = filedialog. askdirectory()
            if len(self.PATH) != 0:
                if type == "<Environment>":
                    self._create_env()
                if type == "<Project>":
                    self._create_project()

                if type == "<App>":
                    self._create_App()
                # subprocess.run('exec.bat')
                from subprocess import Popen
                Popen("exec.bat")

    def _create_env(self):
        ENV_PATH = (self.PATH + '/' + self.FOLDER_NAME)
        f = open('exec.bat', 'w')
        f.write(
            f"""cd "{self.PATH}"\ncall mkvirtualenv {ENV_PATH}\ncall "{ENV_PATH}/Scripts/activate.bat"\npip install django""")
        f.close()

    def _create_project(self):
        f = open('exec.bat', 'w')
        f.write(
            f"""cd "{self.PATH}"\ncall "{self.PATH}/Scripts/activate"\ncall django-admin startproject {self.FOLDER_NAME}\ncd {self.FOLDER_NAME}\nstart http://127.0.0.1:8000/\ncall python manage.py runserver\nexit""")
        f.close()

    def _create_App(self):
        f = open('exec.bat', 'w')
        f.write(
            f"""cd "{self.PATH}"\ncall "{self.PATH}/Scripts/activate"\ncall django-admin startapp "{self.FOLDER_NAME}"\ncall python manage.py migrate\nstart http://127.0.0.1:8000/\ncall python manage.py runserver\nexit""")
        f.close()

    def box(self, root, image="menuscreen.png"):

        global screenheight
        global screenwidth

        # Loading images
        image1 = Image.open(image)
        image_active = str(image[:-(len(".png"))] + "Active" + ".png")
        image1_active = Image.open(image_active)

        # setting window size
        width, height = image1.size
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.overrideredirect(1)
        root.resizable(width=False, height=False)

        # Init image_files
        background = ImageTk.PhotoImage(image1)
        background_active = ImageTk.PhotoImage(image1_active)

        # Position image in label
        label1 = Label(image=background,
                       relief="sunken", borderwidth=0)
        label1.image = background
        label1.place(x=0, y=0)

        # bind drag n drop
        label1.bind("<ButtonPress-1>",
                    lambda event: self.StartMove(root, event))
        label1.bind("<ButtonRelease-1>",
                    lambda event: self.StopMove(root, event))
        label1.bind("<B1-Motion>", lambda event: self.OnMotion(root, event))

        # Bind Window activation
        root.bind("<ButtonPress-1>", lambda x: self.change_image(
            label1, background_active))
        root.bind("<ButtonRelease-1>", lambda x: self.change_image(
            label1, background))

        return label1

    def StartMove(self, root, event):
        root.x = event.x
        root.y = event.y

    def StopMove(self, root, event):
        root.x = None
        root.y = None

    def OnMotion(self, root, event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry("+%s+%s" % (x, y))


root = Tk()
run = App(root)
