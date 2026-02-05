import tkinter as tk
import time
import json
import os

def load_next_time():
    path = os.path.join(os.getcwd(), "next_popup.json")
    try:
        with open(path, "r") as f:
            return json.load(f)["timestamp"]
    except:
        return None

root = tk.Tk()
root.title("Study Nudge 😈")
root.geometry("520x340")
root.attributes("-topmost", True)

label = tk.Label(root, text="Waiting...", font=("Arial", 12))
label.pack(expand=True)

def update_timer():
    target = load_next_time()
    if target:
        remaining = int(target - time.time())
        if remaining < 0:
            label.config(text="Popup incoming 😈")
        else:
            mins = remaining // 60
            secs = remaining % 60
            label.config(text=f"Next popup in {mins:02d}:{secs:02d}")
    root.after(1000, update_timer)

update_timer()
root.mainloop()
