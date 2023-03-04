from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import os

'''
  GUI file to fire front car system 
'''


# call back function to do action for button
def call_back():
    print("hello world")
    # os.system('python main.py')


class Gui:
    def __init__(self):
        # create main window and set title and back ground
        main_window = Tk()
        main_window.title("Front car")
        main_window.geometry("1500x850")
        main_window.configure(background="#73dfed")
        #main_window.attributes("-fullscreen", True)
        # main_window.resizable(0, 0)

        image = ImageTk.PhotoImage(file='img.jpg')
        canvas = Canvas(main_window, width=1000, height=850)
        canvas.pack(expand=True, fill=BOTH)
        # Add the image in the canvas
        canvas.create_image(0, 0, image=image, anchor="nw")

        # create label for page address
        page_address = Label(font=('vendor', 28, 'bold'), text=' V2V Front car ',background="#AFD1EE")
        page_address.place(relx=.5, rely=.15, anchor="center")

        # configure style for button
        style = Style()
        style.configure('TButton', font=('calibre', 22, 'bold'), borderwidth='5',background="#AFD1EE")
        style.map('TButton', foreground=[('active', 'green')],
                  background=[('active', "green")])

        # create Xtra vue button
        xtra_vue_button = Button(main_window, text="XtraVue", command=call_back, width=13)
        xtra_vue_button.place(relx=.5, rely=.5, anchor="center")

        main_window.mainloop()


gui = Gui()
