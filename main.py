from flask import Flask, render_template, url_for, request, g, redirect
import sqlite3

app = Flask(__name__)



@app.route("/")
def home():
    return render_template('index.html')


@app.route("/take",  methods=["POST", "GET"])
def take():
    db = get_db()
    cursor = db.cursor()
    if(request.method == "GET"):
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                quizTitle TEXT,
                description TEXT
            );
        ''')
        res = cursor.execute("SELECT * FROM quizzes").fetchall()
        
        return render_template("take.html", quizzes = res)


@app.route("/take-quiz/<int:quiz_number>",  methods=["POST", "GET"])
def takeQuiz(quiz_number):
    db = get_db()
    cursor = db.cursor()

    if(request.method == "POST"):
        return render_template("score.html")


    if(request.method == "GET"):
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                quizID INT,
                question TEXT,
                a TEXT,
                b TEXT,
                c TEXT,
                d TEXT,
                answer TEXT
            );
        ''')
        res = cursor.execute(f"SELECT * FROM questions WHERE quizID = {quiz_number}").fetchall()
        return render_template("take-quiz.html", quiz_number = quiz_number, questions=res)
    
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
    db = get_db()
    cursor = db.cursor()
    if(request.method == "POST"):
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                quizID INT,
                question TEXT,
                a TEXT,
                b TEXT,
                c TEXT,
                d TEXT,
                answer TEXT
            );
        ''')
        question = request.form.get("question")
        a = request.form.get("a")
        b = request.form.get("b")
        c = request.form.get("c")
        d = request.form.get("d")
        answer  = request.form.get("answer")
        cursor.execute('''
        INSERT INTO questions (quizID, question, a, b, c, d, answer)
        VALUES (?, ?, ?, ?, ?, ?, ?);''', (quiz_number, question, a, b, c, d, answer))
        db.commit()
        return redirect(url_for('editQuiz', quiz_number=quiz_number))


    if(request.method  == "GET"):
        cursor.execute( '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                quizID INT,
                question TEXT,
                a TEXT,
                b TEXT,
                c TEXT,
                d TEXT,
                answer TEXT
            );
        ''')
        res = cursor.execute(f"SELECT * FROM questions WHERE quizID = {quiz_number}").fetchall()
        return render_template('edit-quiz.html', quiz_number=quiz_number, questions = res)
    
@app.route("/score", methods=["POST", "GET"])
def score():
    return render_template("score.html")


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