import os
from engine.pdf_reader import extract_text
from engine.cleaner import clean_text, split_sentences
from engine.question_generator import generate_questions, save_questions

PDF_PATH = "input.pdf"

if not os.path.exists(PDF_PATH) or os.path.getsize(PDF_PATH) == 0:
    raise RuntimeError("input.pdf is missing or empty. Please select a PDF first.")

raw_text = extract_text(PDF_PATH)
cleaned = clean_text(raw_text)
sentences = split_sentences(cleaned)

questions = generate_questions(sentences)
save_questions(questions)

print(f"Saved {len(questions)} questions to questions.json")
