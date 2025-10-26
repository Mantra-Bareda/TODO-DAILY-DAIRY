import customtkinter as ctk
import os
import encrypter as enc
from datetime import date

# Extras
which_file = ""
task_list = []
filenameeeee = ""

def add_hover_effects(button, hover_color="#78C3FB", normal_color="#0E5CFF", Text_colour_hover="#303633", normal_text="#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color, text_color=Text_colour_hover)
    def on_leave(event):
        button.configure(fg_color=normal_color, text_color=normal_text)
    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

def get_files_in_folder(folder_path):
    global which_file, filenameeeee
    files_list = []
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith('.txt') or '.' not in file_name:
                files_list.append(file_name)
    if len(files_list) == 0:
        n = "task-" + str(date.today()) + ".txt"
        new_file_path = os.path.join(folder_path, n)
        with open(new_file_path, "w") as file_to_open:
            pass
        files_list.append(n)
        get_files_in_folder("data/tasks")
    which_file = os.path.join("data\\tasks", files_list[0])
    filenameeeee = files_list[0]
    load_task(files_list[0])
    return files_list

def load_task(f):
    global which_file, task_list, filenameeeee, writing_for
    wf = os.path.join("data\\tasks", f)
    with open(wf, "r") as file_temp:
        d = file_temp.readlines()
    save_in_file()
    task_list = []
    blank_tasks()
    which_file = os.path.join("data\\tasks", f)
    filenameeeee = f
    for i in d:
        if "," in i:
            t, s = i.split(",")
            t = enc.decrypt(t.strip())
            s = s.strip()[0]
            s = True if s == "1" else False
            add_to_list(t, s)
    writing_for.configure(text=f"Current List:{filenameeeee}")

def blank_tasks():
    global scrollable_frame1
    for i in scrollable_frame1.winfo_children():
        if i == writing_for:
            continue
        i.destroy()
    canvas1.configure(scrollregion=canvas1.bbox("all"))

def clear_btns():
    global scrollable_frame3
    for i in scrollable_frame3.winfo_children():
        if i == list_of_files:
            continue
        i.destroy()

def del_task(t):
    del_entry.delete(0, ctk.END)
    for x in range(len(task_list)):
        if task_list[x][0] == t:
            task_list.pop(x)
            break
    save_in_file()
    load_task(filenameeeee)

def add_to_list(t, s=False):
    global task_list
    if t.strip() == "":
        return
    cb = ctk.CTkCheckBox(scrollable_frame1, text=t)
    task_list.append((t, cb))
    cb.select() if s else cb.deselect()
    cb.place(x=0, y=int((task_list.index((t, cb)) * 30) + 33))
    save_in_file()
    task_entry.delete(0, ctk.END)
    canvas1.configure(scrollregion=canvas1.bbox("all"))
    scrollable_frame1.update_idletasks()

def del_file():
    global task_list
    f = which_file
    if os.path.exists(f):
        os.remove(f)
    clear_btns()
    task_list = []
    blank_tasks()
    make_btns()

def save_in_file():
    global which_file, task_list
    with open(which_file, "w") as f:
        for i in task_list:
            t, cb = i
            f.write(f"{enc.encrypt(t)} , {cb.get()}\n")

def make_btns():
    global btns, scrollable_frame3
    btns = []
    files = get_files_in_folder("data/tasks")
    for i in files:
        bt = ctk.CTkButton(scrollable_frame3, text=i, font=("Times New Roman", 16, "bold"), fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda x=i: [load_task(x)])
        add_hover_effects(bt)
        btns.append(bt)
    pos_y = 0
    for i in btns:
        i.place(x=25, y=pos_y+40)
        pos_y += 30

def mk_new_file():
    global new_file_entry
    x = new_file_entry.get()
    if not x.endswith(".txt"):
        x += ".txt"
    with open(os.path.join("data\\tasks", x), "w") as f:
        pass
    new_file_entry.delete(0, ctk.END)
    clear_btns()
    make_btns()

def main_task():
    global win, left_frame, middle_frame, writing_for, right_frame, scrollable_frame1, scrollable_frame3, task_entry, new_file_entry, list_of_files, del_entry, canvas1

    win = ctk.CTk()
    win.geometry("750x500+100+100")
    win.resizable(False, False)
    win.title("To-Do-List")
    win.configure(fg_color="#303633", bg_color="#303633")

    left_frame = ctk.CTkFrame(win, width=297, height=500, bg_color="#303633")
    middle_frame = ctk.CTkFrame(win, width=247, height=500, bg_color="#303633")
    right_frame = ctk.CTkFrame(win, width=197, height=500, bg_color="#303633")

    separator_left_middle = ctk.CTkCanvas(win, width=3, height=500, bg="#7FB069")
    separator_middle_right = ctk.CTkCanvas(win, width=3, height=500, bg="#7FB069")

    task_entry = ctk.CTkEntry(middle_frame, width=200, text_color="#7FB069", font=("Times New Roman", 16, "bold"), placeholder_text="Enter Task")
    del_entry = ctk.CTkEntry(middle_frame, width=200, text_color="#7FB069", font=("Times New Roman", 16, "bold"))
    new_file_entry = ctk.CTkEntry(middle_frame, width=200, text_color="#7FB069", font=("Times New Roman", 16, "bold"), placeholder_text="Enter file name")

    add_bt = ctk.CTkButton(middle_frame, width=200, font=("Times New Roman", 16, "bold"), text="Add task", fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: [add_to_list(task_entry.get())])
    del_bt = ctk.CTkButton(middle_frame, width=200, font=("Times New Roman", 16, "bold"), text="Delete task", fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: [del_task(del_entry.get())])
    del_file_bt = ctk.CTkButton(middle_frame, width=200, font=("Times New Roman", 16, "bold"), text="Delete Current File", fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: [del_file()])
    save_bt = ctk.CTkButton(middle_frame, width=200, font=("Times New Roman", 16, "bold"), text="Save List", fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: [save_in_file()])
    new_file_bt = ctk.CTkButton(middle_frame, width=200, font=("Times New Roman", 16, "bold"), text="Create new file", fg_color="#0E5CFF", text_color="#CCF5AC", command=lambda: [mk_new_file()])

    canvas1 = ctk.CTkCanvas(left_frame, width=297, height=510, bg="#7FB069")
    canvas3 = ctk.CTkCanvas(right_frame, width=200, height=510, bg="#7FB069")

    scrollbar1 = ctk.CTkScrollbar(left_frame, bg_color="#303633", orientation="vertical", command=canvas1.yview, height=500)
    scrollable_frame1 = ctk.CTkFrame(canvas1, width=297, bg_color="#303633", height=505)

    scrollbar3 = ctk.CTkScrollbar(right_frame, bg_color="#303633", orientation="vertical", command=canvas3.yview, height=505)
    scrollable_frame3 = ctk.CTkFrame(canvas3, bg_color="#303633", height=505)

    scrollable_frame1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
    scrollable_frame3.bind("<Configure>", lambda e: canvas3.configure(scrollregion=canvas3.bbox("all")))

    canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
    canvas1.configure(yscrollcommand=scrollbar1.set)

    canvas3.create_window((0, 0), window=scrollable_frame3, anchor="nw")
    canvas3.configure(yscrollcommand=scrollbar3.set)

    writing_for = ctk.CTkLabel(scrollable_frame1, text_color="#7FB069", font=("Times New Roman", 20, "bold"), text=f"Current List:{filenameeeee}")
    list_of_files = ctk.CTkLabel(scrollable_frame3, text_color="#7FB069", font=("Times New Roman", 20, "bold", "underline"), text="To-Do Lists")

    left_frame.place(x=0, y=0)
    separator_left_middle.place(x=297, y=0)
    middle_frame.place(x=300, y=0)
    separator_middle_right.place(x=547, y=0)
    right_frame.place(x=550, y=0)

    canvas1.place(x=-2, y=-5)
    scrollbar1.place(x=282, y=0)

    canvas3.place(x=0, y=-5)
    scrollbar3.place(x=185, y=0)

    pos_x_2 = 25
    pos_y_2 = 0

    task_entry.place(x=pos_x_2, y=10 + pos_y_2)
    del_entry.place(x=pos_x_2, y=150 + pos_y_2)
    add_bt.place(x=pos_x_2, y=45 + pos_y_2)
    del_bt.place(x=pos_x_2, y=180 + pos_y_2)
    del_file_bt.place(x=pos_x_2, y=220 + pos_y_2)
    save_bt.place(x=pos_x_2, y=80 + pos_y_2)
    new_file_entry.place(x=pos_x_2, y=410 + pos_y_2)
    new_file_bt.place(x=pos_x_2, y=450 + pos_y_2)

    writing_for.place(x=0, y=3)
    list_of_files.place(x=40, y=3)

    add_hover_effects(save_bt)
    add_hover_effects(add_bt)
    add_hover_effects(new_file_bt)
    add_hover_effects(del_file_bt)
    add_hover_effects(del_bt)

    make_btns()
    scrollable_frame1.update_idletasks()

    win.mainloop()

# Start App
main_task()
