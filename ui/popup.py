import tkinter as tk
import json

QUESTIONS_PATH = "questions.json"
PROGRESS_PATH = "progress.json"


def load_questions():
    try:
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def load_progress():
    try:
        with open(PROGRESS_PATH, "r") as f:
            return json.load(f).get("index", 0)
    except:
        return 0


def save_progress(index):
    with open(PROGRESS_PATH, "w") as f:
        json.dump({"index": index}, f)


def show_popup(root):
    questions = load_questions()
    if not questions:
        return

    index = load_progress()
    if index >= len(questions):
        index = 0

    q = questions[index]

    popup = tk.Toplevel(root)
    popup.title("Study Nudge 😈")
    popup.geometry("500x300")
    popup.grab_set()
    popup.attributes("-topmost", True)

    tk.Label(
        popup,
        text=q["question"],
        wraplength=450,
        font=("Arial", 11)
    ).pack(pady=20)

    answer_var = tk.StringVar()
    entry = tk.Entry(popup, textvariable=answer_var, width=40)
    entry.pack(pady=10)
    entry.focus()

    feedback = tk.Label(popup, text="")
    feedback.pack(pady=5)

    def submit():
        if answer_var.get().strip().lower() == q["answer"].lower():
            save_progress(index + 1)
            popup.destroy()
        else:
            feedback.config(text="Wrong. Try again 😈", fg="red")

    tk.Button(popup, text="Submit", command=submit).pack(pady=10)
