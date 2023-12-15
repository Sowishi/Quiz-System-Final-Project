from flask import Flask, render_template, url_for, request, g, redirect
import sqlite3
import random


app = Flask(__name__)



@app.route("/")
def home():
    invalid = request.args.get('invalid', default='', type=str)
    return render_template('index.html', invalid=invalid)

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)

    if(username == "admin" and password == "admin"):
        return redirect(url_for('createQuiz'))
    return redirect(url_for('home', invalid=True))


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f"DELETE FROM quizzes where id = {id} ")
    cursor.execute(f"DELETE FROM questions where quizID = {id} ")
    cursor.execute( '''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY,
            quizTitle TEXT,
            description TEXT
        );
    ''')
    res = cursor.execute("SELECT * FROM quizzes").fetchall()
    db.commit()
    return redirect(url_for("createQuiz", quizzes = res, bgColor=generate_random_color))

        
    

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
        
        return render_template("take.html", quizzes = res,  bgColor=generate_random_color)


@app.route("/take-quiz/<int:quiz_number>",  methods=["GET"])
def takeQuiz(quiz_number):
    db = get_db()
    cursor = db.cursor()

    if(request.method == "GET"):
        quiz_title = request.args.get('quizTitle', default='', type=str)
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
        return render_template("take-quiz.html", quiz_number = quiz_number, questions=res, quiz_title=quiz_title, )
    
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

        
        return render_template("create.html", quizzes = res, bgColor=generate_random_color
)

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
    
@app.route("/score/<int:quiz_number>", methods=["POST", "GET"])
def score(quiz_number):
    db = get_db()
    cursor = db.cursor()
    if(request.method == "POST"):
        res = cursor.execute(f"SELECT * FROM questions WHERE quizID = {quiz_number}").fetchall()

        numberOfQuestions = len(res)
        answers = []
        rightAnswers = []
        score = 0

        for i in range(1, numberOfQuestions + 1):
            answers.append(request.form.get(str(i)))

        for question in res:
            rightAnswers.append(question[7])


        for x in range(len(answers)):
            if(answers[x] == rightAnswers[x]):
                score += 1        

        return render_template("score.html", score=score, numberOfQuestions=numberOfQuestions, questions=res)

def generate_random_color():
    # Generate a random hexadecimal color code
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color
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