import os
from app_paths import data_file
from engine.pdf_reader import extract_text
from engine.web_reader import extract_text_from_url
from engine.cleaner import clean_text, split_sentences
from engine.question_generator import generate_questions, save_questions


def generate_questions_from_pdf(pdf_path, questions_path=None):
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
        raise RuntimeError("input.pdf is missing or empty. Please select a PDF first.")

    raw_text = extract_text(pdf_path)
    cleaned = clean_text(raw_text)
    sentences = split_sentences(cleaned)

    questions = generate_questions(sentences)
    output_path = questions_path or str(data_file("questions.json"))
    save_questions(questions, output_path)
    return len(questions), output_path


if __name__ == "__main__":
    count, output = generate_questions_from_pdf(str(data_file("input.pdf")))
    print(f"Saved {count} questions to {output}")
