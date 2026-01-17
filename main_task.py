## Imports
import customtkinter as ctk
import os 
import encrypter as enc
from tkinter import scrolledtext
from datetime import datetime
from tkextrafont import Font

## BASIC THINGS
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
current_file = str()
current_data = []
APP_NAME = "diary_planner"

## Functions

## Get app data path and 3 lines extra things.....
def get_data_dir():
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR = get_data_dir()
TASK_DIR = os.path.join(DATA_DIR, "tasks")
os.makedirs(TASK_DIR, exist_ok=True)


## 1. HOVER FUNCTION TO ADD HOVER EFFECT TO BUTTONS
def add_hover_effects(button, hover_color="#78C3FB", normal_color="#1F538D" , Text_colour_hover = "#303633" , normal_text = "#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color , text_color= Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color = normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

## 2. Get Encrypted data and Decrypt it
def get_data(file_name):
    global current_data
    file_path = os.path.join(TASK_DIR,file_name)

    if(os.path.exists(file_path)):

        data = []

        with open(file_path, "r") as f:
            for line in f:
                data.append(line.rstrip("\n"))

        for i in range(len(data)):
            x = data[i].split(",")
            x[0] = enc.decrypt(x[0])
            x[1] = int(x[1])
            data[i] = x
        
        current_data = data
        return data

## 3. Get File List available in Folder
def file_list():

    folder_name = TASK_DIR
    files = [
        f for f in os.listdir(folder_name)
        if os.path.isfile(os.path.join(folder_name, f))
    ]
                    
    return files

## 4. Delete File and Update list
def file_delete(file_nm):
    file_path = os.path.join(TASK_DIR , file_nm)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    file_list_show(True)

## 5. Show Files List in Frame3
def file_list_show(b=False):
    global frame3 , current_file
    for i in frame3.winfo_children():
        i.destroy()

    d = file_list()

    if len(d)==0 or b==True:
        new_file()

    btns = []

    frame3.columnconfigure(0, weight=1)

    label = ctk.CTkLabel(frame3 , text="File List : ")
    label.grid(row=0 , column=0)

    for r,i in enumerate(d):
        row_frame = ctk.CTkFrame(frame3)
        row_frame.grid(row=r+1, column=0, sticky="ew", pady=5)

        bt = ctk.CTkButton(row_frame , text = i , command=lambda x=i:[task_show(x)])
        bt2 = ctk.CTkButton(row_frame , text = "Delete" , command=lambda x1=i:[file_delete(x1)])

        row_frame.columnconfigure(0, weight=7)
        row_frame.columnconfigure(1, weight=3)

        bt.grid(row=0, column=0, sticky="w", padx=10)

        bt2.grid(row=0, column=1,sticky="e", padx=5)

    if b==True:  
        d_str = "task-"+str(datetime.today().date())+".txt"
        file_path = os.path.join(TASK_DIR , d_str)
        current_file=d_str
        task_show(d_str)

## 6. Make a new File at Start of Program
def new_file():
    global current_file

    d = "task-"+str(datetime.today().date())+".txt"
    file_path = os.path.join(TASK_DIR , d)

    if not os.path.exists(file_path):
        with open(file_path , "w") as f:
            pass

    current_file = d

    file_list_show()
    task_show(current_file)

## 7. Delete Data and Update file and Task List
def delete_task(task_nm , file_nm , data):
    global current_data
    for r , (t,s) in enumerate(data):
        if t==task_nm:
            data.pop(r)
    
    current_data = data
    update_file(file_nm , data)

## 8. Delete Data and Update file and Task List
def add_task(task_nm , file_nm , data):
    global current_data
    if len(task_nm)==0:
        return 0
    
    add_task_entry.delete(0,"end")
    data.append([task_nm,0])

    current_data = data
    update_file(file_nm , data)

## 9. Write Data in File
def update_file(file_nm , data):
    
    with open(os.path.join(TASK_DIR,file_nm) , "w") as f:
        for i in data:
            f.write(f"{enc.encrypt(i[0])},{i[1]}\n")

    task_show(file_nm)

## 10. Function to update data when checkbox ticked
def checbox_ticked(i, file_nm , data,var):
    up = var[i].get()
    data[i][1] = up
    
    with open(os.path.join(TASK_DIR,file_nm) , "w") as f:
        for i in data:
            f.write(f"{enc.encrypt(i[0])},{i[1]}\n")

    task_show(file_nm)

## 11. Show Data in Tkinter Frame 1 According to File_name
def task_show(file_nm):
    global frame1 , current_data, current_file
    
    widgets = frame1.winfo_children()

    for i in widgets:
        i.destroy()

    frame1.columnconfigure(0, weight=1)

    data = get_data(file_nm)
    current_data = data
    current_file = file_nm
    shown = []
    checkboxs = []
    vars = []
    
    label= ctk.CTkLabel(frame1 , text=f"FILE : {file_nm}")
    label.grid(row=0 , column = 0 , sticky="w")

    for r , (t,s) in enumerate(data):
        row_frame = ctk.CTkFrame(frame1)

        row_frame.grid(row=r+1, column=0, sticky="ew", pady=5)

        row_frame.columnconfigure(0, weight=7)
        row_frame.columnconfigure(1, weight=3)

        v = ctk.IntVar(value=s)
        c = ctk.CTkCheckBox(row_frame , text=t ,variable=v,command=lambda i=r:[checbox_ticked(i, file_nm , data,vars)])

        d_button = ctk.CTkButton(row_frame , text = "Delete" ,command=lambda tk = t:[delete_task(tk , file_nm , data)])

        vars.append(v)
        checkboxs.append(c)

        c.grid(row=0, column=0, sticky="w", padx=10)

        d_button.grid(row=0, column=1,sticky="e", padx=5)

## 12. Create a new File and open that file
def create_new_file(file_nm):
    if len(file_nm)==0:
        return 0
    file_path = os.path.join(TASK_DIR , file_nm)
    if not os.path.exists(file_path):
        with(open(file_path , "w")) as f:
            pass
    else:pass
    file_list_show()
    task_show(file_nm) 

## 13. Main Function - to manage all things
def main():
    global root, container, frame1, frame2, frame3 , add_task_entry

    root = ctk.CTk()
    root.title("To-Do-List")
    root.geometry("1200x600+88+50")
    root.configure(bg_color = "#303633")

    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True)

    frame1 = ctk.CTkScrollableFrame(container)
    frame1.pack(side="left", fill="both", expand=True)

    frame2 = ctk.CTkFrame(container)
    frame2.pack(side="left", fill="both", expand=True)


    frame2.grid_columnconfigure(0, weight=2)    
    frame2.grid_columnconfigure(1, weight=6)
    frame2.grid_columnconfigure(2, weight=2)

    frame2.grid_rowconfigure(0, weight=0, minsize=50)
    frame2.grid_rowconfigure(4, weight=0, minsize=200)

    add_task_label = ctk.CTkLabel(frame2 , text= "Add Task : ", font=("Times new Roman",20))
    add_task_label.grid(row=1 , column=1)

    add_task_entry = ctk.CTkEntry(frame2)
    add_task_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

    add_task_button = ctk.CTkButton(frame2 , text = "Add" , command=lambda: [add_task(add_task_entry.get() , current_file , current_data)])
    add_task_button.grid(row=3 , column=1)

    new_file_label = ctk.CTkLabel(frame2 , text= "New File : ", font=("Times new Roman",20))
    new_file_label.grid(row=5 , column=1)

    new_file_entry = ctk.CTkEntry(frame2)
    new_file_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=10)

    create_file_button = ctk.CTkButton(frame2 , text = "Create new File" , command=lambda:[create_new_file(new_file_entry.get())])
    create_file_button.grid(row=7 , column=1)


    frame3 = ctk.CTkScrollableFrame(container)
    frame3.pack(side="left", fill="both", expand=True)


    new_file()



    root.mainloop()
