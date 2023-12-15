from flask import Flask, render_template, url_for, request, g, redirect
import sqlite3

app = Flask(__name__)



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        question = request.form.get("question")
        a = request.form.get("a")
        b = request.form.get("b")
        c = request.form.get("c")
        d = request.form.get("d")
        questionWithAnswer = {
            "question": question,
            "a":a,
            "b": b,
            "c": c,
            "d": d
        }

        print(questionWithAnswer)


        return render_template('create.html')
    elif request.method == "GET":
        return render_template('create.html')

@app.route("/take")
def take():
    return render_template('take.html')


@app.route("/create-quiz", methods=["POST", "GET"])
def createQuiz():
    db = get_db()
    cursor = db.cursor()
    if(request.method == "POST"):
        title = request.form.get("title")
        description = request.form.get("description")
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                quizTitle TEXT,
                description TEXT
            );
        ''')
        cursor.execute( "INSERT INTO quizzes (quizTitle, description) VALUES (?, ?);", (title, description))
        db.commit()
        return redirect(url_for('createQuiz'))

    if(request.method == "GET"):
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                quizTitle TEXT,
                description TEXT
            );
        ''')
        res = cursor.execute("SELECT * FROM quizzes").fetchall()
        
        return render_template("create.html", quizzes = res)

@app.route("/edit-quiz/<int:quiz_number>", methods=["POST", "GET"])
def editQuiz(quiz_number):

    if(request.method == "POST"):
        print("test")

    if(request.method  == "GET"):
        return render_template('edit-quiz.html', quiz_number=quiz_number)
    

# Database Connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("quiz-app.db")
        # db.row_factory = sqlite3.Row
    return db

# close database
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()





if __name__ == "__main__":
    app.run(debug=True)