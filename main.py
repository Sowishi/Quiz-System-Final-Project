from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/create")
def create():
    return render_template('create.html')


@app.route("/take")
def take():
    return render_template('take.html')



if __name__ == "__main__":
    app.run(debug=True)