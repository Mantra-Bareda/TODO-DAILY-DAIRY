import os
import sys
import customtkinter as ctk
from tkinter import scrolledtext
import calendar
from datetime import datetime
import encrypter as enc
from tkinter import messagebox
from tkextrafont import Font


APP_NAME = "diary_planner"

def get_data_dir():
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR = get_data_dir()
DIARY_DIR = os.path.join(DATA_DIR, "diary_entries")
os.makedirs(DIARY_DIR, exist_ok=True)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

current_date = datetime.now()
selected_date = current_date


def add_hover_effects(button, hover_color="#78C3FB", normal_color="#1F538D",
                      Text_colour_hover="#303633", normal_text="#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color, text_color=Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color=normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

def add_hover_effects_new(button, hover_color="#FFD6A5", normal_color="#E8F0FE", 
                          Text_colour_hover="#3A2E1F", normal_text="#2A2F45"):
    def on_hover(event):
        button.configure(fg_color=hover_color, text_color=Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color=normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

def ency(s):
    return "".join(chr(ord(i) + 4) for i in s)

def decy(s):
    return "".join(chr(ord(i) - 4) for i in s)


def create_calendar(root, calendar_frame, text_area, date_label, year, month):
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    prev_month_button = ctk.CTkButton(
        calendar_frame, text="<<", width=30, height=30,
        font=("Arial", 16, "bold"),
        fg_color="#0E5CFF", text_color="#CCF5AC",
        command=lambda: change_month(root, calendar_frame, text_area, date_label, year, month - 1)
    )
    prev_month_button.grid(row=0, column=0, padx=5, pady=5)

    next_month_button = ctk.CTkButton(
        calendar_frame, text=">>", width=30, height=30,
        font=("Arial", 16, "bold"),
        fg_color="#0E5CFF", text_color="#CCF5AC",
        command=lambda: change_month(root, calendar_frame, text_area, date_label, year, month + 1)
    )
    next_month_button.grid(row=0, column=6, padx=5, pady=5)

    month_year_label = ctk.CTkLabel(
        calendar_frame,
        text=f"{calendar.month_name[month]} {year}",
        font=font_month,
        text_color="#7FB069"
    )
    month_year_label.grid(row=0, column=1, columnspan=5, pady=10)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        ctk.CTkLabel(calendar_frame, text=day,
                     text_color="#7FB069",
                     font=font_week).grid(row=1, column=i, padx=5, pady=5)

    cal = calendar.monthcalendar(year, month)
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            if day != 0:
                btn = ctk.CTkButton(calendar_frame,text=str(day),width=30,height=30,font=("Times New Roman", 16, "bold"),fg_color="#0E5CFF",text_color="#CCF5AC",command=lambda d=day, y=year, m=month:
                        on_date_click(root, calendar_frame, text_area, date_label, d, y, m))
                
                if(check_file_exist_or_not(day,year,month)):
                    btn.configure(fg_color = "#E8F0FE",text_color="#2A2F45")
                    add_hover_effects_new(btn)
                else:add_hover_effects(btn)

                btn.grid(row=week_num + 2, column=day_num, padx=5, pady=5)

                if (day == selected_date.day and
                        month == selected_date.month and
                        year == selected_date.year):
                    btn.configure(fg_color="#1F6AA5")

def change_month(root, calendar_frame, text_area, date_label, year, month):
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    create_calendar(root, calendar_frame, text_area, date_label, year, month)

def on_date_click(root, calendar_frame, text_area, date_label, day, year, month):
    global selected_date
    save_entry(text_area)
    text_area.after(100, text_area.focus_set)
    selected_date = datetime(year, month, day)
    date_label.configure(text=f"Writing for: {selected_date.strftime('%Y-%m-%d')}")
    create_calendar(root, calendar_frame, text_area, date_label, year, month)
    load_entry(text_area)

def check_file_exist_or_not(day , year , month):
    date_local_var = datetime(year , month , day)
    if os.path.exists(os.path.join(DIARY_DIR, date_local_var.strftime("%Y-%m-%d.txt"))):return True
    else:return False


def load_entry(text_area):
    file_path = os.path.join(DIARY_DIR, selected_date.strftime("%Y-%m-%d.txt"))
    text_area.delete(1.0, ctk.END)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            text_area.insert(ctk.INSERT, decy(file.read().lstrip()))

def save_entry(text_area):
    file_path = os.path.join(DIARY_DIR, selected_date.strftime("%Y-%m-%d.txt"))
    text_content = text_area.get(1.0, ctk.END).strip()

    if text_content:
        with open(file_path, "w") as file:
            file.write(ency(text_content))
    else:
        if os.path.exists(file_path):
            os.remove(file_path)

def auto_save(event, text_area):
    save_entry(text_area)

def main():
    global text_area, save_button, date_label, font_month, font_week

    root = ctk.CTk()
    root.title("Daily Diary")
    root.geometry("1200x600+88+50")
    root.resizable(False, False)
    root.configure(bg_color="#303633")

    calendar_frame = ctk.CTkFrame(root, width=200, corner_radius=10, bg_color="#303633")
    calendar_frame.place(x=10, y=10)

    font_month = ctk.CTkFont(family="Times new Roman", size=30, weight="bold", underline=True)
    font_week = ctk.CTkFont(family="Times new Roman", size=15, underline=True)
    font_date = ctk.CTkFont(family="Times new Roman", size=20, slant="italic")

    text_area = scrolledtext.ScrolledText(root, wrap=ctk.WORD, width=85, height=12,bg="#2E2E2E", fg="#7FB069",font=("Times new Roman" ,15),spacing1=10, spacing2=5,spacing3=10)
    text_area.place(x=298, y=30)

    date_label = ctk.CTkLabel(root,text=f"Writing for: {selected_date.strftime('%d-%m-%y')}",font=font_date,text_color="#b0cac7")
    date_label.place(x=300, y=0)

    save_button = ctk.CTkButton(root, text="Save", command=lambda: save_entry(text_area))
    save_button.place(x=298, y=570)
    add_hover_effects(save_button)

    create_calendar(root, calendar_frame, text_area, date_label,
                    current_date.year, current_date.month)
    load_entry(text_area)

    text_area.bind("<KeyRelease>", lambda event: auto_save(event, text_area))
    text_area.after(100, text_area.focus_set)

    root.mainloop()