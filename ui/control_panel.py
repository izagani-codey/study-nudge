import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os
import json
import threading
import time
from ui.popup import show_popup

# -------------------- GLOBAL STATE --------------------
CONFIG_PATH = "config.json"
selected_pdf = None

scheduler_thread = None
scheduler_running = False
next_popup_time = None


# -------------------- CONFIG HELPERS --------------------
def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return {
            "mode": "fixed",
            "fixed_minutes": 45,
            "enabled": False,
            "language_mode": "english"
        }

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


# -------------------- SCHEDULER LOGIC --------------------
def scheduler_loop():
    global scheduler_running, next_popup_time

    while scheduler_running:
        cfg = load_config()

        if not cfg.get("enabled", False):
            time.sleep(1)
            continue

        wait = (
            cfg["fixed_minutes"] * 60
            if cfg["mode"] == "fixed"
            else 60
        )

        next_popup_time = time.time() + wait

        for _ in range(wait):
            if not scheduler_running:
                return
            time.sleep(1)

        if scheduler_running:
            root.after(0, lambda: show_popup(root))


# -------------------- UI ACTIONS --------------------
def start_scheduler():
    global scheduler_thread, scheduler_running

    cfg = load_config()
    cfg["enabled"] = True
    save_config(cfg)

    if not scheduler_running:
        scheduler_running = True
        scheduler_thread = threading.Thread(
            target=scheduler_loop,
            daemon=True
        )
        scheduler_thread.start()

    status_label.config(text="Status: RUNNING", fg="green")


def stop_scheduler():
    global scheduler_running, next_popup_time

    cfg = load_config()
    cfg["enabled"] = False
    save_config(cfg)

    scheduler_running = False
    next_popup_time = None

    status_label.config(text="Status: STOPPED", fg="red")


def set_language_mode(value):
    cfg = load_config()
    cfg["language_mode"] = value
    save_config(cfg)


# -------------------- PDF HANDLING --------------------
def select_pdf():
    global selected_pdf

    file_path = filedialog.askopenfilename(
        title="Select a PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file_path:
        selected_pdf = file_path
        pdf_label.config(text=f"Selected: {os.path.basename(file_path)}")


def generate_questions():
    if not selected_pdf:
        messagebox.showwarning("No PDF", "Please select a PDF first.")
        return

    target_path = os.path.join(os.getcwd(), "input.pdf")

    with open(selected_pdf, "rb") as src, open(target_path, "wb") as dst:
        dst.write(src.read())

    if os.path.getsize(target_path) == 0:
        messagebox.showerror("PDF Error", "Copied PDF is empty.")
        return

    subprocess.run(["python", "main.py"])
    messagebox.showinfo("Done", "Questions generated successfully!")


# -------------------- UI SETUP --------------------
root = tk.Tk()
root.title("Study Nudge – Control Panel")
root.geometry("500x400")

title = tk.Label(root, text="Study Nudge Control Panel", font=("Arial", 14))
title.pack(pady=10)

btn_select = tk.Button(root, text="Select PDF", command=select_pdf)
btn_select.pack(pady=5)

pdf_label = tk.Label(root, text="No PDF selected")
pdf_label.pack(pady=5)

btn_generate = tk.Button(root, text="Generate Questions", command=generate_questions)
btn_generate.pack(pady=10)

status_label = tk.Label(root, text="Status: STOPPED", fg="red")
status_label.pack(pady=10)

btn_start = tk.Button(root, text="▶ Start Study Mode", command=start_scheduler)
btn_start.pack(pady=5)

btn_stop = tk.Button(root, text="⏹ Stop Study Mode", command=stop_scheduler)
btn_stop.pack(pady=5)

lang_label = tk.Label(root, text="Language Mode:")
lang_label.pack(pady=5)

lang_var = tk.StringVar(value=load_config().get("language_mode", "english"))
lang_menu = ttk.Combobox(
    root,
    textvariable=lang_var,
    values=["english", "dhivehi", "mixed"],
    state="readonly",
    width=15
)
lang_menu.pack(pady=5)
lang_menu.bind("<<ComboboxSelected>>", lambda e: set_language_mode(lang_var.get()))

timer_label = tk.Label(root, text="Next popup: --:--", font=("Arial", 11))
timer_label.pack(pady=10)


# -------------------- TIMER UPDATE --------------------
def update_timer():
    if next_popup_time:
        remaining = int(next_popup_time - time.time())
        if remaining <= 0:
            timer_label.config(text="Popup incoming 😈")
        else:
            m, s = divmod(remaining, 60)
            timer_label.config(text=f"Next popup in {m:02d}:{s:02d}")
    else:
        timer_label.config(text="Next popup: --:--")

    root.after(1000, update_timer)


update_timer()


# -------------------- INITIAL STATE SYNC --------------------
cfg = load_config()
if cfg.get("enabled", False):
    status_label.config(text="Status: RUNNING", fg="green")


root.mainloop()
