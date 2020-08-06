from flask import render_template, redirect, url_for
from flask_login import login_user, current_user
from clubmatcher import app, db, bcrypt
from clubmatcher.forms import ClubForm, QuizForm
from clubmatcher.models import Club


@app.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))
    form = ClubForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        club = Club(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            twitter=form.twitter.data,
            website=form.website.data
        )
        if form.ecommerce.data:
            club.ecommerce = form.ecommerce.data
        db.session.add(club)
        db.session.commit()
        login_user(club)
        return redirect(url_for('quiz'))
    return render_template(
        'pages/register.html',
        title='Register Your Club',
        form=form
    )

@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )
