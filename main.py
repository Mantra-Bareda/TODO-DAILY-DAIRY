import encrypter as enc
import customtkinter as ctk
import os
from tkinter import messagebox
import main_diary
import main_task
import shutil
import tkinter as tk
from datetime import date
from tkinter import filedialog
import sys


APP_NAME = "diary_planner"

def get_data_dir():
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR = get_data_dir()
DIARY_DIR = os.path.join(DATA_DIR, "diary_entries")
TASK_DIR = os.path.join(DATA_DIR, "tasks")
CONFIG_FILE = os.path.join(DATA_DIR, "config.txt")

os.makedirs(DIARY_DIR, exist_ok=True)
os.makedirs(TASK_DIR, exist_ok=True)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def check_folders():
    os.makedirs(DIARY_DIR, exist_ok=True)
    os.makedirs(TASK_DIR, exist_ok=True)

def login_check():
    global CHECK_RESULT
    CHECK_RESULT = ""

    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            p = enc.decrypt(f.read())
            CHECK_RESULT = str(pw.get()) == p
    else:
        with open(CONFIG_FILE, "w") as f:
            f.write(enc.encrypt(pw.get()))
        CHECK_RESULT = True

    win.destroy()

def change_pass1():
    new_pass_entry.place(x=250, y=250)
    bt5.place(x=250, y=275)

def change_pass2():
    with open(CONFIG_FILE, "w") as f:
        f.write(enc.encrypt(new_pass_entry.get()))

    new_pass_entry.place_forget()
    bt5.place_forget()

def make_backup():
    a = select_folder()
    if not a:
        return

    zip_file_path = os.path.join(a, f'data_{date.today()}')
    shutil.make_archive(zip_file_path, 'zip', DATA_DIR)

    Label_backup_done.place(x=250, y=200)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected

def add_hover_effects(button, hover_color="#78C3FB", normal_color="#1F538D",Text_colour_hover="#303633", normal_text="#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color, text_color=Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color=normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

def on_enter(event):
    login_check()

def login():
    global win, pw
    check_folders()

    win = ctk.CTk()
    win.title("Login Window")
    win.geometry("500x500+100+100")
    win.resizable(False, False)
    win.configure(bg_color="#303633")

    label = ctk.CTkLabel(win, text="Login Window",font=("Times New Roman", 40),text_color="#7FB069")
    label.place(x=125, y=200)

    win.bind("<Return>", on_enter)

    pw_label = ctk.CTkLabel(win, font=("Times New Roman", 16),text_color="#7FB069",text="Enter Password : ")
    pw_label.place(x=125, y=300)

    pw = ctk.CTkEntry(win, show="*", width=150, text_color="#78C3FB")
    pw.place(x=230, y=300)
    pw.after(100, pw.focus_set)

    check_bt = ctk.CTkButton(win, text="Check",font=("Times New Roman", 16),command=login_check)
    add_hover_effects(check_bt)
    check_bt.place(x=200, y=350)

    win.mainloop()

def main():
    global Label_backup_done, new_pass_entry, bt5

    login()
    a = CHECK_RESULT

    if a is False:
        messagebox.showinfo("Wrong Credentials")
        return

    root = ctk.CTk()
    root.geometry("500x500+50+50")
    root.resizable(False, False)
    root.title("Multi-Things")

    bt1 = ctk.CTkButton(root, text="Daily Diary",font=("Times New Roman", 16),text_color="#CCF5AC",command=main_diary.main)

    bt1.place(x=100, y=100)

    bt2 = ctk.CTkButton(root, text="To-Do-List",font=("Times New Roman", 16),text_color="#CCF5AC",command=main_task.main)
    bt2.place(x=100, y=150)

    bt3 = ctk.CTkButton(root, text="Backup",font=("Times New Roman", 16),text_color="#CCF5AC",command=make_backup)
    bt3.place(x=100, y=200)

    bt4 = ctk.CTkButton(root, text="Change Password",font=("Times New Roman", 16),text_color="#CCF5AC",command=change_pass1)
    bt4.place(x=100, y=250)

    new_pass_entry = ctk.CTkEntry(root)

    bt5 = ctk.CTkButton(root, text="Change",font=("Times New Roman", 16),text_color="#CCF5AC",command=change_pass2)

    Label_backup_done = ctk.CTkLabel(root,font=("Times New Roman", 16),text="Backup done !!!")

    for b in (bt1, bt3, bt4, bt5):
        add_hover_effects(b)

    root.mainloop()

main()
