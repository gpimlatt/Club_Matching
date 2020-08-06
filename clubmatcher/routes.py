from flask import render_template, redirect, url_for
from clubmatcher import app
from clubmatcher.forms import ClubForm


@app.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = ClubForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template(
        'pages/register.html',
        title='Register Your Club',
        form=form
    )
