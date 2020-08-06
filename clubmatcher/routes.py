from flask import render_template
from clubmatcher import app


@app.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )
