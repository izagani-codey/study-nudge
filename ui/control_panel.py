import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import json
import threading
import time
from app_paths import data_file
from main import generate_questions_from_pdf
from ui.popup import show_popup

CONFIG_PATH = data_file("config.json")
INPUT_PDF_PATH = data_file("input.pdf")

selected_pdf = None
scheduler_thread = None
scheduler_running = False
next_popup_time = None
root = None
status_label = None
pdf_label = None
interval_var = None
timer_label = None
lang_var = None


def _default_config():
    return {
        "mode": "fixed",
        "fixed_minutes": 45,
        "enabled": False,
        "language_mode": "english",
        "last_pdf": None,
    }


def load_config():
    cfg = _default_config()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, dict):
                cfg.update(loaded)
    except Exception:
        pass
    return cfg


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def scheduler_loop():
    global scheduler_running, next_popup_time

    while scheduler_running:
        cfg = load_config()

        if not cfg.get("enabled", False):
            next_popup_time = None
            time.sleep(1)
            continue

        wait = max(1, int(cfg.get("fixed_minutes", 45))) * 60
        next_popup_time = time.time() + wait

        while scheduler_running:
            cfg = load_config()
            if not cfg.get("enabled", False):
                next_popup_time = None
                break

            remaining = int(next_popup_time - time.time())
            if remaining <= 0:
                root.after(0, lambda: show_popup(root))
                break

            time.sleep(1)


def start_scheduler():
    global scheduler_thread, scheduler_running

    cfg = load_config()
    cfg["enabled"] = True
    save_config(cfg)

    if not scheduler_running:
        scheduler_running = True
        scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
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


def set_interval_minutes(_event=None):
    raw = interval_var.get().strip()
    try:
        minutes = int(raw)
        if minutes < 1 or minutes > 240:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid interval", "Use a whole number from 1 to 240 minutes.")
        interval_var.set(str(load_config().get("fixed_minutes", 45)))
        return

    cfg = load_config()
    cfg["fixed_minutes"] = minutes
    save_config(cfg)


def select_pdf():
    global selected_pdf

    file_path = filedialog.askopenfilename(
        title="Select a PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file_path:
        selected_pdf = file_path
        cfg = load_config()
        cfg["last_pdf"] = file_path
        save_config(cfg)
        pdf_label.config(text=f"Selected: {os.path.basename(file_path)}")


def _load_last_pdf_from_config():
    global selected_pdf

    cfg = load_config()
    last_pdf = cfg.get("last_pdf")
    if last_pdf and os.path.exists(last_pdf):
        selected_pdf = last_pdf
        pdf_label.config(text=f"Selected: {os.path.basename(last_pdf)}")


def generate_questions():
    if not selected_pdf:
        messagebox.showwarning("No PDF", "Please select a PDF first.")
        return

    with open(selected_pdf, "rb") as src, open(INPUT_PDF_PATH, "wb") as dst:
        dst.write(src.read())

    if os.path.getsize(INPUT_PDF_PATH) == 0:
        messagebox.showerror("PDF Error", "Copied PDF is empty.")
        return

    try:
        count, output_path = generate_questions_from_pdf(str(INPUT_PDF_PATH))
    except Exception as exc:
        messagebox.showerror("Generation failed", str(exc))
        return

    messagebox.showinfo("Done", f"Generated {count} questions\nSaved to: {output_path}")


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


def run_control_panel():
    global root, status_label, pdf_label, interval_var, timer_label, lang_var

    root = tk.Tk()
    root.title("Study Nudge – Control Panel")
    root.geometry("520x470")

    cfg = load_config()

    tk.Label(root, text="Study Nudge Control Panel", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Select PDF", command=select_pdf).pack(pady=5)

    pdf_label = tk.Label(root, text="No PDF selected")
    pdf_label.pack(pady=5)

    tk.Button(root, text="Generate Questions", command=generate_questions).pack(pady=10)

    status_label = tk.Label(root, text="Status: STOPPED", fg="red")
    status_label.pack(pady=10)

    interval_frame = tk.Frame(root)
    interval_frame.pack(pady=4)

    tk.Label(interval_frame, text="Popup interval (minutes):").pack(side="left", padx=(0, 8))
    interval_var = tk.StringVar(value=str(cfg.get("fixed_minutes", 45)))
    interval_entry = tk.Entry(interval_frame, textvariable=interval_var, width=8)
    interval_entry.pack(side="left")
    interval_entry.bind("<Return>", set_interval_minutes)

    tk.Button(interval_frame, text="Apply", command=set_interval_minutes).pack(side="left", padx=8)

    tk.Button(root, text="▶ Start Study Mode", command=start_scheduler).pack(pady=5)
    tk.Button(root, text="⏹ Stop Study Mode", command=stop_scheduler).pack(pady=5)

    tk.Label(root, text="Language Mode:").pack(pady=5)

    lang_var = tk.StringVar(value=cfg.get("language_mode", "english"))
    lang_menu = ttk.Combobox(
        root,
        textvariable=lang_var,
        values=["english", "dhivehi", "mixed"],
        state="readonly",
        width=15,
    )
    lang_menu.pack(pady=5)
    lang_menu.bind("<<ComboboxSelected>>", lambda e: set_language_mode(lang_var.get()))

    timer_label = tk.Label(root, text="Next popup: --:--", font=("Arial", 11))
    timer_label.pack(pady=10)

    update_timer()
    _load_last_pdf_from_config()

    if cfg.get("enabled", False):
        status_label.config(text="Status: RUNNING", fg="green")
        start_scheduler()

    root.mainloop()


if __name__ == "__main__":
    run_control_panel()
