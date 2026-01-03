import customtkinter as ctk
from tkinter import messagebox

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


def main_notepad():
    
    root = ctk.Ctk()
    


    root.mainloop()
