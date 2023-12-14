from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('quiz-app.db')
cursor = conn.cursor()



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
    if request.method == "POST":
   
        title = request.form.get("title")

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                quizTitle TEXT NOT NULL
            );
        """)

        # Insert the quiz title using a parameterized query
        cursor.execute(f"INSERT INTO quizzes (quizTitle) VALUES ({title})")

        # Commit the changes to the database
        conn.commit()

        return render_template("create.html")
    else:
        return render_template("create.html")








if __name__ == "__main__":
    app.run(debug=True)