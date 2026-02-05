import json

SKIP_WORDS = ["the", "a", "an", "is", "are", "to", "of", "and"]

def choose_keyword(words):
    candidates = [
        w for w in words
        if w.lower() not in SKIP_WORDS and len(w) > 5
    ]

    if not candidates:
        return None

    return candidates[len(candidates) // 2]


def generate_questions(sentences, max_questions=5):
    questions = []

    ranked = sorted(sentences, key=len, reverse=True)
    important = ranked[:max_questions]

    for sentence in important:
        words = sentence.split()
        answer = choose_keyword(words)

        if answer:
            question = sentence.replace(answer, "_____ ", 1)
            questions.append({
                "type": "fill_blank",
                "question": question,
                "answer": answer
            })

    return questions


def save_questions(questions, path="questions.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
