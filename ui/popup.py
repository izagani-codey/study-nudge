import tkinter as tk
import json
import re

QUESTIONS_PATH = "questions.json"
PROGRESS_PATH = "progress.json"


def load_questions():
    try:
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def load_progress():
    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("index", 0)
    except Exception:
        return 0


def save_progress(index):
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump({"index": index}, f)


def normalize_answer(value):
    value = value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^\w\s]", "", value)
    return value


def show_popup(root):
    questions = load_questions()
    if not questions:
        return

    index = load_progress()
    if index >= len(questions):
        index = 0

    q = questions[index]
    expected_answer = str(q.get("answer", ""))

    popup = tk.Toplevel(root)
    popup.title("Study Nudge 😈")
    popup.geometry("560x360")
    popup.grab_set()
    popup.attributes("-topmost", True)

    tk.Label(
        popup,
        text=f"Question {index + 1} of {len(questions)}",
        font=("Arial", 10, "italic")
    ).pack(pady=(12, 4))

    tk.Label(
        popup,
        text=q.get("question", ""),
        wraplength=510,
        justify="left",
        font=("Arial", 11)
    ).pack(padx=20, pady=(4, 14))

    answer_var = tk.StringVar()
    entry = tk.Entry(popup, textvariable=answer_var, width=56)
    entry.pack(pady=6)
    entry.focus_set()

    feedback = tk.Label(popup, text="Type your answer and press Enter.", fg="gray")
    feedback.pack(pady=6)

    attempts = {"count": 0}

    def submit(_event=None):
        user_answer = normalize_answer(answer_var.get())
        correct_answer = normalize_answer(expected_answer)

        if user_answer and user_answer == correct_answer:
            save_progress(index + 1)
            popup.destroy()
            return

        attempts["count"] += 1
        if attempts["count"] >= 2:
            feedback.config(
                text=f"Not quite. Expected answer: {expected_answer}",
                fg="orange"
            )
        else:
            feedback.config(text="Wrong. Try once more.", fg="red")

    def skip_question():
        save_progress(index + 1)
        popup.destroy()

    entry.bind("<Return>", submit)

    btn_row = tk.Frame(popup)
    btn_row.pack(pady=12)

    tk.Button(btn_row, text="Submit", command=submit, width=12).pack(side="left", padx=6)
    tk.Button(btn_row, text="Skip", command=skip_question, width=12).pack(side="left", padx=6)
