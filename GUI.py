import customtkinter as ctk
from tkinter import *
from tkinterdnd2 import *
from PIL import Image, ImageTk
from MusicClassifier import *
from Utils import *

file = ''
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def get_path(event):
    input.insert('end', event.data)

root = Tk()
icon = Image.open(ICON_PATH)
photo = ImageTk.PhotoImage(icon)
root.geometry(SIZE)
root.title(TITLE)
root.iconphoto(True,photo)

#main frame can scroll
main_frame = ctk.CTkScrollableFrame(root,
                                   width = 800,
                                   height = 1000,)
                                   #label_text = 'Music Genre Classification',
                                   #label_fg_color = 'pink',
                                   #label_font=("Roboto",30, "bold"))
main_frame.pack(pady=0)

bg_im = ctk.CTkImage(light_image=Image.open("gui_images\\bgd.jpg"), 
                     dark_image= Image.open("gui_images\\bgd.jpg"),
                     size = (800, 300))
bg_label = ctk.CTkLabel(main_frame, image= bg_im, text= "")
bg_label.pack()

#change light/dark mode
mode ="dark"
def change():
    global mode
    if mode == "dark":
        ctk.set_appearance_mode("light")
        mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        mode="dark"


change_button = ctk.CTkButton(main_frame, text="Change Mode", command= change)
change_button.pack(pady=5, anchor="e")

first_font = ctk.CTkFont(family="Urbani", size = 25, weight= "bold")
first_label = ctk.CTkLabel(main_frame, text= "Wanna know your music's type ?", font =first_font) 
first_label.pack(pady = 30)

#input 
input_label = ctk.CTkLabel(main_frame, text = "Drop your music file here", font = ("Urbani", 12))
input_label.pack(pady=0)

input = ctk.CTkTextbox(main_frame, width = 600, height = 100, corner_radius=30)
input.pack(pady=5)

input.drop_target_register(DND_FILES)
input.dnd_bind('<<Drop>>', get_path)

#result 
def result():
    global file
    file = input.get(0.0, 'end').split('\n')[0]
    audio_genre = audio_process(file)
    result_win = ctk.CTkToplevel(root)
    result_win.title("Result Window")
    result_win.geometry('400x300')
    result_win.iconbitmap(ICON_PATH)
    result_win.resizable(False, False)

    result_label = ctk.CTkLabel(result_win, text= f'Random Forest: {audio_genre[0]}\nKNN: {audio_genre[1]}\nLogistic Regression: {audio_genre[2]}', font = result_font)
    result_label.pack(pady= 40)

    def back():
        result_win.destroy()
        result_win.update()
        reset()

    #close window
    close_button = ctk.CTkButton(result_win, text="Turn back!", font = ("Urbani", 12), command= back)
    close_button.pack(pady=20)

result_font = ctk.CTkFont(family="Urbani", size = 14, weight="bold")
result_button = ctk.CTkButton(main_frame,text="Show Result", font= result_font, width=80, height=50, corner_radius=50, command = result)
result_button.pack(pady = 15)

#reset
def reset():
    input.delete(0.0, 'end')

reset_button = ctk.CTkButton(main_frame, text = "Delete",font = ("Urbani", 10),width=50, height= 30, corner_radius= 50, command=reset)
reset_button.pack(pady = 0)

#picture frame
pic_frame = ctk.CTkFrame(main_frame, width = 800, height = 400)
pic_frame.pack(pady=10)

pic1 = ctk.CTkImage(light_image=Image.open("gui_images\\app1.webp"),
                    dark_image=Image.open("gui_images\\app1.webp"),
                    size = (300, 150))
pic1_label = ctk.CTkLabel(pic_frame, image=pic1, text="")
pic1_label.grid(row=0, column=1, padx = 10, pady = 10)

pic2 = ctk.CTkImage(light_image=Image.open("gui_images\\pic2.jpg"),
                    dark_image=Image.open("gui_images\\pic2.jpg"),
                    size = (80, 150))
pic2_label = ctk.CTkLabel(pic_frame, image=pic2, text="")
pic2_label.grid(row=0, column=0, padx = 20, pady = 10)

pic3 = ctk.CTkImage(light_image=Image.open("gui_images\\pic3.jpg"),
                    dark_image=Image.open("gui_images\\pic3.jpg"),
                    size = (80, 150))
pic3_label = ctk.CTkLabel(pic_frame, image=pic3, text="")
pic3_label.grid(row=0, column=2, padx = 20, pady = 10)

#import images
image_frame = ctk.CTkFrame(main_frame, width= 800, height = 500)
image_frame.pack(pady= 20)

image1 = ctk.CTkImage(light_image=Image.open('gui_images\\blues.png'),
                    dark_image=Image.open('gui_images\\blues.png'),
                    size = (170, 80))
image_label1 = ctk.CTkLabel(image_frame, image=image1, text="")
image_label1.grid(row = 1, column= 0, padx= 10, pady = 10)

image2 = ctk.CTkImage(light_image=Image.open('gui_images\\classical.png'),
                    dark_image=Image.open('gui_images\\classical.png'),
                    size = (170, 80))
image_label2 = ctk.CTkLabel(image_frame, image=image2, text="")
image_label2.grid(row = 1, column= 1, padx= 10, pady = 10)

image3 = ctk.CTkImage(light_image=Image.open('gui_images\\country.png'),
                    dark_image=Image.open('gui_images\\country.png'),
                    size = (170, 80))
image_label3 = ctk.CTkLabel(image_frame, image=image3, text="")
image_label3.grid(row = 1, column= 2, padx= 10, pady = 10)

image4 = ctk.CTkImage(light_image=Image.open('gui_images\\jazz.png'),
                    dark_image=Image.open('gui_images\\jazz.png'),
                    size = (170, 80))
image_label4 = ctk.CTkLabel(image_frame, image=image4, text="")
image_label4.grid(row = 1, column= 3, padx= 10, pady = 10)

#space = ctk.CTkLabel(main_frame, text="kkk")
#space.pack(pady=10, side="bottom")

image5 = ctk.CTkImage(light_image=Image.open('gui_images\\metal.png'),
                    dark_image=Image.open('gui_images\\metal.png'),
                    size = (170, 80))
image_label5 = ctk.CTkLabel(image_frame, image=image5, text="")
image_label5.grid(row = 2, column= 0, padx= 10, pady = 10)

image6 = ctk.CTkImage(light_image=Image.open('gui_images\\pop.png'),
                    dark_image=Image.open('gui_images\\pop.png'),
                    size = (170, 80))
image_label6 = ctk.CTkLabel(image_frame, image=image6, text="")
image_label6.grid(row = 2, column= 1, padx= 10, pady = 10)

image7 = ctk.CTkImage(light_image=Image.open('gui_images\\reggae.png'),
                    dark_image=Image.open('gui_images\\reggae.png'),
                    size = (170, 80))
image_label7 = ctk.CTkLabel(image_frame, image=image7, text="")
image_label7.grid(row = 2, column= 2, padx= 10, pady = 10)

image8 = ctk.CTkImage(light_image=Image.open('gui_images\\rock.png'),
                    dark_image=Image.open('gui_images\\rock.png'),
                    size = (170, 80))
image_label8 = ctk.CTkLabel(image_frame, image=image8, text="")
image_label8.grid(row = 2, column= 3, padx= 10, pady = 10)

#use intro frame
use_intro_frame = ctk.CTkFrame(main_frame, width = 650, height= 100)
use_intro_frame.pack(pady= 20)

#how to use
use_frame = ctk.CTkFrame(use_intro_frame, width = 300, height = 100)
use_frame.grid(row=0, column = 0, padx=10, pady = 5)

use_title_font = ctk.CTkFont(family="Urbani", size = 20, weight= "bold")

title_use_label = ctk.CTkLabel(use_frame, text = "How to use", font= use_title_font)
title_use_label.pack(pady = 5)

text_use_label = ctk.CTkLabel(use_frame, text = "Using '.wav' files and drop it to the text box above \n"
                                                + "and the System will show you the type that your music belongs to", font = ("Urbani", 12), anchor="w")
text_use_label.pack(pady= 5)

#Introduction
intro_frame = ctk.CTkFrame(use_intro_frame, width = 300, height = 100)
intro_frame.grid(row=0, column=1, padx=10, pady = 5)

intro_label = ctk.CTkLabel(intro_frame, text = "What is this system use for", font = use_title_font)
intro_label.grid(row= 0, column = 0, padx = 5, pady=5)

intro_text_label = ctk.CTkLabel(intro_frame, text = "This System using Machine Learing techniques to analyse \n and classify music into 10 categories.\n Whenever you input your music file, the System will predict\n which categories that it belongs to", font = ("Urbani", 12), anchor="w")
intro_text_label.grid(row= 1, column = 0, padx = 5, pady=5, sticky="w")

'''
#Information_frame
info_frame = ctk.CTkFrame(main_frame, width = 800, height = 300, fg_color="blue")

info_frame.pack(pady = 20, side="bottom", fill="both")
'''
root.mainloop()