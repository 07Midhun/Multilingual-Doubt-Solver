from flask import Flask, Blueprint, render_template, request
import pandas as pd
import os

# Create blueprint
main_blueprint = Blueprint('main', __name__, template_folder='templates')

# Homepage
@main_blueprint.route('/')
def home():
    return render_template('index.html')

# Doubt Solver page
@main_blueprint.route('/ask')
def ask():
    return render_template('ask.html')

# Quiz selection page
@main_blueprint.route('/quiz')
def quiz():
    return render_template('quiz.html')

# Start quiz by reading Excel file
@main_blueprint.route('/start_quiz', methods=['POST'])
def start_quiz():
    subject = request.form.get('subject')       # e.g., 'math'
    language = request.form.get('language')     # e.g., 'en'
    selected_class = request.form.get('class')  # e.g., '1'
    difficulty = request.form.get('difficulty') # e.g., 'easy'

    filename = f"data/class{selected_class}{subject}{difficulty}.xlsx"

    if not os.path.exists(filename):
        return f"Quiz file '{filename}' not found!", 404

    df = pd.read_excel(filename)

    questions = []
    for _, row in df.iterrows():
        questions.append({
            'q': row['question'],
            'options': [row['option1'], row['option2'], row['option3'], row['option4']],
            'answer': row['answer']
        })

    return render_template(
        'quiz_questions.html',
        questions=questions,
        subject=subject,
        selected_class=selected_class,
        difficulty=difficulty
    )

# Submit quiz and calculate score
@main_blueprint.route('/submit_quiz', methods=['POST'])

def submit_quiz():
    subject = request.form.get("subject")
    selected_class = request.form.get("selected_class")
    difficulty = request.form.get("difficulty")

    # Load the same Excel file again to access correct answers
    filepath = f"data/class{selected_class}{subject}{difficulty}.xlsx"

    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        return f"Error loading quiz file: {e}", 500

    score = 0
    user_answers = []
    correct_answers = df['answer'].tolist()
    questions = df['q'].tolist()

    # Compare submitted answers with correct ones
    for i in range(len(questions)):
        user_ans = request.form.get(f'q{i}')
        user_answers.append(user_ans)

        if user_ans and user_ans.strip().lower() == str(correct_answers[i]).strip().lower():
            score += 1

    return render_template(
        'quiz_result.html',
        score=score,
        total=len(questions),
        user_answers=user_answers,
        correct_answers=correct_answers,
        questions=questions
    )

# Main Flask app
app = Flask(__name__)
app.secret_key = "secret123"
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
