import os
import customtkinter as ctk
from tkinter import scrolledtext
import calendar
from datetime import datetime
import encrypter as enc
from tkinter import messagebox
from tkextrafont import Font
import tkextrafont

_january_font = None

def get_january_font():
    global _january_font
    if _january_font is None:
        _january_font = Font(
            file="fonts\\January Night.ttf",
            family="January Night",
            size=15
        )
    return _january_font

_abasalom = None

def get_abasalom_font():
    global _abasalom
    if _abasalom is None:
        _abasalom = Font(file="fonts\\new\\Abasalomdemo-ax8Am.otf" )
    return _abasalom






ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

file_location = "data/diary_entries"
if not os.path.exists(file_location):
    os.makedirs(file_location)

current_date = datetime.now()
selected_date = current_date

def add_hover_effects(button, hover_color="#78C3FB", normal_color="#0E5CFF" , Text_colour_hover = "#303633" , normal_text = "#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color , text_color= Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color = normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

def ency(s):
    s_2 = ""

    for i in s:
        x = ord(i)
        x = x+4
        s_2 += chr(x)

    return s_2

def decy(s):
    s_2 = ""
    for i in s:
        x = ord(i)
        x-=4
        s_2 += chr(x)
    return s_2

def create_calendar(root, calendar_frame, text_area, date_label, year, month):
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    # Create the navigation buttons (Previous and Next month)
    prev_month_button = ctk.CTkButton(calendar_frame, text="<<", width=30, height=30, font=("Arial", 16, "bold"),
                                      fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: change_month(root, calendar_frame, text_area, date_label, year, month - 1))
    prev_month_button.grid(row=0, column=0, padx=5, pady=5)

    next_month_button = ctk.CTkButton(calendar_frame, text=">>", width=30, height=30, font=("Arial", 16, "bold"),
                                      fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: change_month(root, calendar_frame, text_area, date_label, year, month + 1))
    next_month_button.grid(row=0, column=6, padx=5, pady=5)

    # Adjust the position of the month-year label
    month_year_label = ctk.CTkLabel(calendar_frame, text=f"{calendar.month_name[month]} {year}", font=font_month, text_color="#7FB069")
    month_year_label.grid(row=0, column=1, columnspan=5, pady=10)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        ctk.CTkLabel(calendar_frame, text=day, text_color="#7FB069", font=font_week ).grid(row=1, column=i, padx=5, pady=5)

    cal = calendar.monthcalendar(year, month)  # Get the month view (cal is a list of weeks)
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            if day != 0:
                # Modify the button to pass the correct year and month
                btn = ctk.CTkButton(calendar_frame, text=str(day), width=30, height=30, font=("Times New Roman", 16, "bold"), fg_color="#0E5CFF", text_color="#CCF5AC",
                                    command=lambda d=day, y=year, m=month: on_date_click(root, calendar_frame, text_area, date_label, d, y, m))
                add_hover_effects(btn)
                btn.grid(row=week_num + 2, column=day_num, padx=5, pady=5)
                if day == selected_date.day and month == selected_date.month and year == selected_date.year:
                    btn.configure(fg_color="#1F6AA5")



def change_month(root, calendar_frame, text_area, date_label, year, month):
    # Update the year and month if it's valid
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Call create_calendar with the new year and month
    create_calendar(root, calendar_frame, text_area, date_label, year, month)



def on_date_click(root, calendar_frame, text_area, date_label, day, year, month):
    global selected_date
    save_entry(text_area)
    text_area.after(100, text_area.focus_set)
    selected_date = datetime(year, month, day)  # Use the passed year and month here
    date_label.configure(text=f"Writing for: {selected_date.strftime('%Y-%m-%d')}")
    create_calendar(root, calendar_frame, text_area, date_label, year, month)  # Recreate calendar with new date
    load_entry(text_area)


def load_entry(text_area):
    file_path = os.path.join(file_location, selected_date.strftime("%Y-%m-%d.txt"))
    text_area.delete(1.0, ctk.END)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            text_area.insert(ctk.INSERT, decy(file.read().lstrip()))

def save_entry(text_area):
    file_path = os.path.join(file_location, selected_date.strftime("%Y-%m-%d.txt"))
    
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
    global text_area , save_button , date_label , font_month , font_week
    root = ctk.CTk()
    root.title("Daily Diary")
    root.geometry("1200x600+88+50")
    root.resizable(False , False)
    root.configure(bg_color = "#303633")
    root.iconbitmap("icon.ico")
        

    calendar_frame = ctk.CTkFrame(root, width=200, corner_radius=10 , bg_color="#303633")
    calendar_frame.place(x = 10,y = 10)


    font_textarea = get_january_font()
    font_temp_1 = get_abasalom_font()
    family1 ="Abasalom Demo"
    font_month = ctk.CTkFont(family=family1 , size = 30 , weight="bold" , underline=True)
    font_week = ctk.CTkFont(family=family1 , size = 15 , underline=True)
    font_date = ctk.CTkFont(family=family1 , size = 20 ,slant="italic")

    text_area = scrolledtext.ScrolledText(root, wrap=ctk.WORD, width=97, height=14, bg="#2E2E2E", fg="#7FB069", font=font_textarea, spacing1=10, spacing2=5, spacing3=10)
    text_area.place(x = 298 , y = 30)

    date_label = ctk.CTkLabel(root, text=f"Writing for: {selected_date.strftime('%d-%m-%y')}", font=font_date, text_color="#b0cac7")
    date_label.place(x = 300 , y = 0)

    save_button = ctk.CTkButton(root, text="Save", command=lambda: save_entry(text_area))
    save_button.place(x= 298 , y = 570)

    add_hover_effects(save_button)

    create_calendar(root, calendar_frame, text_area, date_label, current_date.year, current_date.month)
    load_entry(text_area)

    text_area.bind("<KeyRelease>", lambda event: auto_save(event, text_area))

    text_area.after(100, text_area.focus_set)

    root.mainloop()
