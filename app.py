from flask import Flask, render_template
from firebase_admin import db
import app_auth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    app_auth.connect_firebase()
    ref = db.reference('/interns')
    intern_scores = ref.get()
    return render_template("index.html", intern_scores=intern_scores)


if __name__ == "__main__":
    app.run()
