from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
