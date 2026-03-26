import tkinter as tk
import json
import re
from app_paths import data_file

QUESTIONS_PATH = data_file("questions.json")
PROGRESS_PATH = data_file("progress.json")


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


def _question_type_label(question_type):
    labels = {
        "mcq": "Multiple Choice",
        "true_false": "True / False",
        "fill_blank": "Fill in the Blank",
    }
    return labels.get(question_type, "Question")


def show_popup(root):
    questions = load_questions()
    if not questions:
        return

    index = load_progress()
    if index >= len(questions):
        index = 0

    q = questions[index]
    expected_answer = str(q.get("answer", ""))
    q_type = q.get("type", "fill_blank")

    popup = tk.Toplevel(root)
    popup.title("Study Nudge 😈")
    popup.geometry("600x430")
    popup.grab_set()
    popup.attributes("-topmost", True)

    tk.Label(
        popup,
        text=f"Question {index + 1} of {len(questions)} • {_question_type_label(q_type)}",
        font=("Arial", 10, "italic")
    ).pack(pady=(12, 4))

    tk.Label(
        popup,
        text=q.get("question", ""),
        wraplength=550,
        justify="left",
        font=("Arial", 11)
    ).pack(padx=20, pady=(4, 14))

    feedback = tk.Label(popup, text="Answer and press Enter.", fg="gray")
    feedback.pack(pady=4)

    answer_var = tk.StringVar()
    attempts = {"count": 0}

    def mark_correct_and_close():
        save_progress(index + 1)
        popup.destroy()

    def is_correct(user_text):
        user = normalize_answer(user_text)
        expected = normalize_answer(expected_answer)
        if not user:
            return False

        if q_type == "true_false":
            user = {"t": "true", "f": "false"}.get(user, user)
            return user == expected

        if q_type == "mcq":
            options = q.get("options", [])
            if user in {"a", "b", "c", "d"}:
                pos = ord(user) - ord("a")
                if 0 <= pos < len(options):
                    user = normalize_answer(str(options[pos]))
            return user == expected

        return user == expected

    def submit(_event=None):
        if is_correct(answer_var.get()):
            mark_correct_and_close()
            return

        attempts["count"] += 1
        if attempts["count"] >= 2:
            feedback.config(text=f"Not quite. Expected answer: {expected_answer}", fg="orange")
        else:
            feedback.config(text="Wrong. Try once more.", fg="red")

    def skip_question():
        save_progress(index + 1)
        popup.destroy()

    if q_type == "mcq":
        options = q.get("options", [])
        if options:
            options_frame = tk.Frame(popup)
            options_frame.pack(pady=(0, 8))
            for idx, option in enumerate(options):
                letter = chr(ord("A") + idx)
                tk.Label(
                    options_frame,
                    text=f"{letter}. {option}",
                    justify="left",
                    anchor="w",
                    font=("Arial", 10)
                ).pack(fill="x", padx=20)
            feedback.config(text="Type the answer text or A/B/C/D, then press Enter.", fg="gray")

    if q_type == "true_false":
        tf_frame = tk.Frame(popup)
        tf_frame.pack(pady=(0, 10))
        tk.Button(tf_frame, text="True", width=10, command=lambda: (answer_var.set("True"), submit())).pack(side="left", padx=5)
        tk.Button(tf_frame, text="False", width=10, command=lambda: (answer_var.set("False"), submit())).pack(side="left", padx=5)

    entry = tk.Entry(popup, textvariable=answer_var, width=58)
    entry.pack(pady=8)
    entry.focus_set()
    entry.bind("<Return>", submit)

    btn_row = tk.Frame(popup)
    btn_row.pack(pady=12)

    tk.Button(btn_row, text="Submit", command=submit, width=12).pack(side="left", padx=6)
    tk.Button(btn_row, text="Skip", command=skip_question, width=12).pack(side="left", padx=6)
