from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def get_answer(question):
    context = "This is a general academic answer system. Extend context for better accuracy."
    result = qa_pipeline(question=question, context=context)
    return result['answer']
