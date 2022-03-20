from flask import Flask, render_template
import leaderboard

app = Flask(__name__)


@app.route('/')
def index():
    intern_scores = leaderboard.get_scores()
    return render_template("index.html", intern_scores=intern_scores)


if __name__ == "__main__":
    app.run()
