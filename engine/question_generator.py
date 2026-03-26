import json
import random
import re
from collections import Counter

SKIP_WORDS = {
    "the", "a", "an", "is", "are", "to", "of", "and", "for", "that", "with",
    "from", "this", "these", "those", "into", "about", "have", "has", "had", "will",
    "can", "could", "should", "would", "their", "there", "they", "them", "were", "been",
}


WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z\-']+")


def _tokenize(sentence):
    return [w for w in WORD_PATTERN.findall(sentence)]


def _is_candidate(word):
    return len(word) >= 5 and word.lower() not in SKIP_WORDS


def _build_vocab(sentences):
    all_words = []
    for sentence in sentences:
        all_words.extend([w.lower() for w in _tokenize(sentence) if _is_candidate(w)])
    return Counter(all_words)


def choose_keyword(sentence, vocab):
    words = _tokenize(sentence)
    candidates = [w for w in words if _is_candidate(w)]

    if not candidates:
        return None

    # Harder questions: prefer rarer, longer domain words.
    def score(word):
        return (
            -vocab.get(word.lower(), 0),
            -len(word),
            word.lower(),
        )

    ranked = sorted(candidates, key=score)
    return ranked[0]


def _replace_whole_word(text, target, replacement):
    pattern = re.compile(rf"\b{re.escape(target)}\b")
    return pattern.sub(replacement, text, count=1)


def _sentence_priority(sentence):
    words = _tokenize(sentence)
    complex_words = [w for w in words if _is_candidate(w)]
    return (len(complex_words), len(words), len(sentence))


def make_fill_blank(sentence, answer):
    masked = _replace_whole_word(sentence, answer, "_____ ")
    return {
        "type": "fill_blank",
        "question": f"Fill in the blank:\n{masked}",
        "answer": answer,
    }


def make_mcq(sentence, answer, distractor_pool, rng):
    mask = _replace_whole_word(sentence, answer, "_____ ")
    choices = [d for d in distractor_pool if d.lower() != answer.lower()]

    if len(choices) < 3:
        return None

    sampled = rng.sample(choices, 3)
    options = sampled + [answer]
    rng.shuffle(options)

    return {
        "type": "mcq",
        "question": f"Choose the best answer:\n{mask}",
        "answer": answer,
        "options": options,
    }


def make_true_false(sentence, answer, distractor_pool, rng):
    # Alternate between true and false variants.
    make_false = bool(rng.randint(0, 1))

    if make_false:
        alternatives = [d for d in distractor_pool if d.lower() != answer.lower()]
        if alternatives:
            replacement = rng.choice(alternatives)
            statement = _replace_whole_word(sentence, answer, replacement)
            return {
                "type": "true_false",
                "question": f"True or False:\n{statement}",
                "answer": "False",
            }

    return {
        "type": "true_false",
        "question": f"True or False:\n{sentence}",
        "answer": "True",
    }


def generate_questions(sentences, max_questions=12, seed=42):
    if not sentences:
        return []

    rng = random.Random(seed)
    vocab = _build_vocab(sentences)

    ranked = sorted(sentences, key=_sentence_priority, reverse=True)
    important = ranked[: max(max_questions * 2, 10)]

    extracted = []
    for sentence in important:
        answer = choose_keyword(sentence, vocab)
        if answer:
            extracted.append((sentence, answer))

    if not extracted:
        return []

    distractor_pool = sorted({a for _, a in extracted}, key=lambda x: (len(x), x.lower()))

    questions = []
    types_cycle = ["mcq", "true_false", "fill_blank"]

    for idx, (sentence, answer) in enumerate(extracted):
        q_type = types_cycle[idx % len(types_cycle)]

        if q_type == "mcq":
            q = make_mcq(sentence, answer, distractor_pool, rng)
            if not q:
                q = make_fill_blank(sentence, answer)
        elif q_type == "true_false":
            q = make_true_false(sentence, answer, distractor_pool, rng)
        else:
            q = make_fill_blank(sentence, answer)

        questions.append(q)
        if len(questions) >= max_questions:
            break

    return questions


def save_questions(questions, path="questions.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
