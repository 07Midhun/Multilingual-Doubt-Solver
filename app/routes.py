from flask import Blueprint, render_template, request
from app.translator import translate_to_en, translate_from_en
from app.qa_model import get_answer

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')
@main_blueprint.route('/ask', methods=['POST'])
def ask():
    original_lang = request.form['lang']
    question = request.form['question']

    translated_question = translate_to_en(question, original_lang)
    answer_en, context_used = get_answer(translated_question)
    answer_local = translate_from_en(answer_en, original_lang)
    context_local = translate_from_en(context_used, original_lang)

    return render_template('result.html', question=question, answer=answer_local, context=context_local, lang=original_lang)

