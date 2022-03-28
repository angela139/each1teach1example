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
    ordered = sorted(intern_scores.items(), key=lambda t:int(t[1]["score"]), reverse=True)
    print(ordered)
    return render_template("index.html", intern_scores=ordered)


if __name__ == "__main__":
    app.run()
