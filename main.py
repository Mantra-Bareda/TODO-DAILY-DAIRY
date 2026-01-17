## BASIC IMPORTS
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


## FUNCTIONS

## 1. CHECKING FOLDER (DATA FOLDER)
def check_folders():
    paths = ["data\\diary_entries" , "data\\tasks"]
    for i in paths:
        if not os.path.exists(i):
            os.mkdir(i)
        else:pass          


## 2. FUNCTION TO CHECK PASSWORD IS CORRECT OR NOT
def login_check():
    global CHECK_RESULT
    CHECK_RESULT = ""
    check= os.path.isfile("data\config.txt")
    if check:
        with open("data\config.txt" , "r") as f:
            p = enc.decrypt(f.read())
            if str(pw.get()) == p:
                CHECK_RESULT= True
            else:
                CHECK_RESULT= False
    else:
        if os.path.isdir("data"):
            shutil.rmtree("data")
            os.makedirs("data")
            with open("data\config.txt" , "w") as f:
                f.write(enc.encrypt(pw.get()))
        else:
            os.makedirs("data")
            with open("data\config.txt" , "w") as f:
                f.write(enc.encrypt(pw.get()))
            
    win.destroy()

## 3. CHANGING PASSWORD 2 FUNCTIONS
def change_pass1():
    new_pass_entry.place(x = 250 , y = 250)
    bt5.place(x = 250 , y = 275)

def change_pass2():
    with open("data\config.txt" , "w") as f:
                f.write(enc.encrypt(new_pass_entry.get()))
    
    new_pass_entry.place_forget()
    bt5.place_forget()



## 4. TAKE BACKUP OF EVERYTHING
def make_backup():
    a = select_folder()
    folder_path = 'data'

    zip_file_path = str(str(a) + "/" + f'data_{date.today()}.zip')

    shutil.make_archive(zip_file_path, 'zip', folder_path)

    Label_backup_done.place(x = 250 , y = 200)    


## 5. SELECTING BACKUP FOLDER
def select_folder():
    root = tk.Tk()
    root.withdraw()  
    folder_selected = filedialog.askdirectory(initialdir="G:/My Drive/backup/mantra/some text file and extra/text/personal")
    return folder_selected


## 6. BIND ENTER KEY TO RUN LOGIN CHECK FUNTION
def on_enter(event):
    login_check()


## 7. LOGIN FUNCTION (CREATE LOGIN WINDOW AND ALL)
def login():
    global win , pw
    check_folders()
    win = ctk.CTk()
    win.title("Login Window")
    win.geometry("500x500+100+100")
    win.resizable(False , False)
    win.configure(bg_color = "#303633")
    win.iconbitmap("icon.ico")
    
    label = ctk.CTkLabel(win , text = "Login Window" ,font=("Times New Roman", 40) , text_color= "#7FB069")
    label.place(x= 125 , y = 200)

    win.bind("<Return>", on_enter)

    pw_label = ctk.CTkLabel(win ,font=("Times New Roman", 16) , text_color="#7FB069", text = "Enter Password : ")
    pw_label.place(x = 125, y = 300)
    pw = ctk.CTkEntry(win , show = "*",width=150 , text_color="#78C3FB")
    pw.place(x=230,y=300)

    pw.after(100, pw.focus_set)
    
    check_bt = ctk.CTkButton(win , text = "Check",font=("Times New Roman", 16) , command=lambda : [login_check()])
    add_hover_effects(check_bt)
    check_bt.place(x=200 , y = 350)

    win.mainloop()

## 8. FUNTION TO ADD A GOOD HOVER EFFECT TO THE BUTTONS THAT ARE PASSED IN FUNCTIONS
def add_hover_effects(button, hover_color="#78C3FB", normal_color="#1F538D" , Text_colour_hover = "#303633" , normal_text = "#CCF5AC"):
    def on_hover(event):
        button.configure(fg_color=hover_color , text_color= Text_colour_hover)

    def on_leave(event):
        button.configure(fg_color=normal_color, text_color = normal_text)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)



## 9. MAIN FUNCTION WITH ALL UI AND OTHER THINGS AND MANAGAGE ALL OTHER FUNTIONS
def main():
    global Label_backup_done , new_pass_entry , bt5

    ## RUN LOGIN FUNCTION
    login()

    ## GET IF PROPER CREDENTIALS
    a = CHECK_RESULT

    ## PROCEED AS PER RESULT
    if a == False:
        messagebox.showinfo("Wrong Credentials")
    else:
        
        ## IF PROPER CREDENTIAL --> RUN FUNCTIONS
        
        ## CREATE A CUSTOM-TKINTER WINDOWS
        root = ctk.CTk()
        root.geometry("500x500+50+50")
        root.resizable(False,False)
        root.title("Multi-Things")
        root.iconbitmap("icon.ico")


        ## CREATE BUTTON -> 1 - DIARY , 2 - TASK , 3 - BACKUP , 4 - CHANGE_PASS , 5 - CHANGE_CONFIRM
        bt1 = ctk.CTkButton(root , text = "Daily Diary" ,font=("Times New Roman", 16),text_color="#CCF5AC", command=lambda:[main_diary.main()])

        bt2 = ctk.CTkButton(root , text = "To-do list",font=("Times New Roman", 16),text_color="#CCF5AC", command=lambda:[main_task.main()])

        bt1.place(x=100 , y =100)

        bt2.place(x=100 , y =150)

        bt3 = ctk.CTkButton(root , text = "Backup" ,font=("Times New Roman", 16),text_color="#CCF5AC", command=lambda : [make_backup()])

        bt3.place(x = 100 , y = 200)

        bt4 = ctk.CTkButton(root , text = "Change Password",font=("Times New Roman", 16),text_color="#CCF5AC" , command = lambda : [change_pass1()])

        bt4.place(x= 100 , y = 250)

        ## ENTRY TO GET NEW PASS
        new_pass_entry = ctk.CTkEntry(root)

        bt5 = ctk.CTkButton(root , text = "Change" ,font=("Times New Roman", 16),text_color="#CCF5AC", command = lambda : [change_pass2()])

        ## LABEL TO SHOW THAT PASSWORD IS CHANGED
        Label_backup_done = ctk.CTkLabel(root,font=("Times New Roman", 16), text = "Backup done !!!")
        

        ## ADDING HOVER EFFECT TO EVERY BUTTON
        add_hover_effects(bt1)
        add_hover_effects(bt2)
        add_hover_effects(bt3)
        add_hover_effects(bt4)
        add_hover_effects(bt5)

        ## RUN THE MAIN WINDOW
        root.mainloop()

main()
