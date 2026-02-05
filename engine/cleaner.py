import re
import json

def load_language_mode():
    try:
        with open("config.json", "r") as f:
            return json.load(f).get("language_mode", "mixed")
    except:
        return "mixed"

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text

def split_sentences(text):
    mode = load_language_mode()
    sentences = text.split(".")
    good = []

    for s in sentences:
        s = s.strip()

        # length filter
        if not (40 < len(s) < 180):
            continue

        # reject examples / instructional junk
        bad_phrases = [
            "brace yourself",
            "as you know",
            "from the previous lesson",
            "notice that",
            "here are",
            "there are quite a few",
            "this means",
            "we will",
            "you can see"
        ]

        if any(p in s.lower() for p in bad_phrases):
            continue

        # language filtering
        non_ascii_ratio = sum(1 for c in s if ord(c) > 127) / len(s)

        if mode == "english" and non_ascii_ratio > 0.05:
            continue

        if mode == "dhivehi" and non_ascii_ratio < 0.20:
            continue

        good.append(s)

    return good
