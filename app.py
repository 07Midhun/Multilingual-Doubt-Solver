from flask import Flask
from app.routes import main_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
