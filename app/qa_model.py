# app/qa_model.py

from transformers import pipeline
from app.data_loader import load_context_file, split_into_chunks, find_best_context

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


# Load textbook once (on app start)
textbook_path = "data/ncert_science_class9.txt"
full_text = load_context_file(textbook_path)
text_chunks = split_into_chunks(full_text)

def get_answer(question):
    if not text_chunks:
        return "No content found.", ""

    best_context = find_best_context(question, text_chunks)
    result = qa_pipeline(question=question, context=best_context)
    return result['answer'], best_context

