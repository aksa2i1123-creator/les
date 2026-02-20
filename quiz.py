# Code for the app
from random import randint
from flask import Flask, session, redirect, url_for
from db_scripts import get_question_after, get_quises

quiz = 0
last_question = 0
def start_quiz(quiz_id):
    """Menyimpan nilai awal quiz di session"""
    session['quiz'] = int(quiz_id)
    session['last_question'] = 0


def end_quiz():
    """Menghapus semua session"""
    session.clear()

def quiz_form():
    """Menampilkan dropdown daftar quiz dari database"""
    
    html_beg = """
    <html>
    <body>
        <h2>Choose a quiz:</h2>
        <form method="post" action="/index">
            <select name="quiz">
    """

    frm_submit = """
            </select>
            <p><input type="submit" value="Select"></p>
        </form>
    </body>
    </html>
    """

    options = ""
    q_list = get_quises()

    for quiz_id, name in q_list:
        option_line = f'<option value="{quiz_id}">{name}</option>'
        options += option_line

    return html_beg + options + frm_submit

def index():
    global quiz, last_question
    max_quiz = 12
    quiz = randint(1, max_quiz)
    return '<a href="/test">Test</a>'
def test():
    global last_question
    result = get_question_after(last_question, quiz)
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        last_question = result[0]
        return '<h1>' + str(quiz) + '<br>' + str(result) + '</h1>'
def result():
    return "Begitulah data yang ada"

app = Flask(__name__)
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)

# ========================
# Setup Flask App
# ========================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)
if __name__ == '__main__':
    # starting the web server:
    app.run()
