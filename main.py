import encrypter as enc
import customtkinter as ctk
from tkinter import messagebox
import main_diary
import main_task
import tkinter as tk
from datetime import date , datetime
from tkinter import filedialog
from pathlib import Path
import zipfile , json , tempfile , shutil , os , hashlib , secrets , getpass


APP_NAME = "diary_planner"
APP_ID = "com.utilityapp.diaryplanner"
BACKUP_VERSION = 1



def get_data_dir():
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


DATA_DIR = get_data_dir()
DIARY_DIR = os.path.join(DATA_DIR, "diary_entries")
TASK_DIR = os.path.join(DATA_DIR, "tasks")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

os.makedirs(DIARY_DIR, exist_ok=True)
os.makedirs(TASK_DIR, exist_ok=True)

def check_before_run():
    if not os.path.exists(os.path.join(CONFIG_FILE)):
        register()
    else:
        with(open(CONFIG_FILE , "r")) as f:
            d = f.read()
            d = enc.decrypt(d)
            if(len(d.strip())==0):
                register()
            else:pass

def register():
    global register_pw , reg_win
    reg_win = ctk.CTk()
    reg_win.geometry("500x500+100+100")
    reg_win.resizable(False , False)
    reg_win.title("Register....")
    reg_win.configure(bg_color="#303633")

    label = ctk.CTkLabel(reg_win, text="Register Window",font=("Times New Roman", 40),text_color="#7FB069")
    label.place(x=125, y=200)

    reg_win.bind("<Return>", on_enter_register)

    pw_label = ctk.CTkLabel(reg_win, font=("Times New Roman", 16),text_color="#7FB069",text="Enter Password : ")
    pw_label.place(x=125, y=300)

    register_pw = ctk.CTkEntry(reg_win, show="*", width=150, text_color="#78C3FB")
    register_pw.place(x=230, y=300)
    register_pw.after(100, register_pw.focus_set)

    check_bt_register = ctk.CTkButton(reg_win, text="Register",font=("Times New Roman", 16),command=register_do)
    add_hover_effects(check_bt_register)
    check_bt_register.place(x=200, y=350)

    reg_win.mainloop()

def register_do():
    global register_pw
    pass_w = register_pw.get()
    if len(pass_w.strip()) == 0:
        messagebox.showerror(title="Enter Something",message="Enter Something then Press Enter") 
        return 0
    else:pass

    with(open(CONFIG_FILE , "w")) as f:
        f.write(enc.encrypt(pass_w))

    reg_win.destroy()


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

def restore_backup():
    global APP_ID , BACKUP_VERSION
    zip_path = select_zip_file()
    if not zip_path:
        return

    APP_ID_verify = APP_ID
    BACKUP_VERSION_verify = BACKUP_VERSION

    if not zipfile.is_zipfile(zip_path):
        raise ValueError("Invalid ZIP file")

    with zipfile.ZipFile(zip_path, "r") as z:
        zip_names = z.namelist()

        if "backup_manifest.json" not in zip_names:
            raise ValueError("Invalid backup: manifest missing")

        manifest = json.loads(
            z.read("backup_manifest.json").decode("utf-8")
        )

        if manifest.get("app_id") != APP_ID_verify:
            raise ValueError("Backup not created by this app")

        if manifest.get("backup_version") != BACKUP_VERSION_verify:
            raise ValueError("Unsupported backup version")

        for item in manifest.get("structure", []):
            if not any(name.startswith(item) for name in zip_names):
                raise ValueError(f"Backup missing required item: {item}")

        rollback_dir = tempfile.mkdtemp(
            prefix="sticky_restore_rollback_"
        )

        shutil.copytree(DATA_DIR,rollback_dir,dirs_exist_ok=True)

        restore_tmp = tempfile.mkdtemp(prefix="sticky_restore_tmp_")

        try:
            z.extractall(restore_tmp)

            for root, dirs, files in os.walk(restore_tmp):
                rel_path = os.path.relpath(root, restore_tmp)
                if rel_path == ".":
                    target_root = DATA_DIR
                else:
                    target_root = os.path.join(DATA_DIR, rel_path)

                os.makedirs(target_root, exist_ok=True)

                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(target_root, file)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)

        except Exception as e:
            shutil.rmtree(DATA_DIR, ignore_errors=True)
            shutil.copytree(
                rollback_dir,
                DATA_DIR,
                dirs_exist_ok=True
            )
            raise RuntimeError(
                f"Restore failed, rolled back: {e}"
            )

        finally:
            shutil.rmtree(restore_tmp, ignore_errors=True)
            shutil.rmtree(rollback_dir, ignore_errors=True)


def make_backup():
    a = select_folder()
    if not a:
        return

    manifest = {
    "app_id": APP_ID,
    "backup_version": BACKUP_VERSION,
    "created_at": datetime.now().isoformat(),
    "structure": [
        "folder1",
        "folder2",
        "config.txt"
    ]
    }
    manifest_path = os.path.join(DATA_DIR, "backup_manifest.json")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    zip_file_path = os.path.join(a, f'data_{date.today()}')
    shutil.make_archive(zip_file_path, 'zip', DATA_DIR)

    os.remove(manifest_path)

    Label_backup_done.place(x=250, y=200)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


def select_zip_file():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askopenfilename(title="Select ZIP file",filetypes=[("ZIP files", "*.zip")])
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

def on_enter_register(event):
    register_do()

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

    check_before_run()

    while True:
        login()
        a = CHECK_RESULT

        if a is False:
            messagebox.showinfo("Wrong Credentials" , "Enter Correct Password")
        else:
            break

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

    bt6 = ctk.CTkButton(root, text="Restore Backup",font=("Times New Roman", 16),text_color="#CCF5AC",command=restore_backup)
    bt6.place(x=100, y=300)

    for b in (bt1,bt2, bt3, bt4, bt5,bt6):
        add_hover_effects(b)

    root.mainloop()

main()
