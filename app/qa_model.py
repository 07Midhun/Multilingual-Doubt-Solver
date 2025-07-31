from transformers import pipeline
from app.data_loader import load_context_file, split_into_chunks, find_best_context

import random
from keybert import KeyBERT
kw_model = KeyBERT()

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
textbook_path = "data/ncert_science_class9.txt"
full_text = load_context_file(textbook_path)
text_chunks = split_into_chunks(full_text)

def get_answer(question):
    text_chunks = split_into_chunks(full_text)
    keywords = [kw[0] for kw in kw_model.extract_keywords(question, top_n=5)]
    filtered_chunks = [chunk for chunk in text_chunks if any(k.lower() in chunk.lower() for k in keywords)]
    if not filtered_chunks:
        filtered_chunks = text_chunks

    best_context = find_best_context(question, filtered_chunks)

    result = qa_pipeline(question=question, context=best_context)
    answer = result['answer']

    return answer, best_context
def generate_mcq(correct_answer):
    distractors = [
        "A form of respiration",
        "A method of evaporation",
        "A way animals breathe",
        "A form of condensation"
    ]
    if correct_answer not in distractors:
        distractors.pop()
        distractors.append(correct_answer)
    return distractors
