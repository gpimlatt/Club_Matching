from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from clubmatcher import app, db, bcrypt
from clubmatcher.forms import ClubForm, QuizForm, LoginForm
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        if club and bcrypt.check_password_hash(club.password, form.password.data):
            login_user(club)
            return redirect(url_for('account'))
    return render_template(
        'pages/login.html',
        title='Login',
        form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template(
        'pages/account.html',
        title='Club Information'
    )


@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        answers = form.q1.data + ',' \
                  + form.q2.data + ',' \
                  + form.q3.data
        if current_user.is_authenticated:
            current_user.answers = answers
            db.session.commit()
        else:
            pass  # record student quiz
        return redirect(url_for('results'))
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )


@app.route("/results", methods=['GET', 'POST'])
def results():
    if current_user.is_authenticated:
        return render_template(
            'pages/club_results.html',
            title='Results'
        )
    else:
        return render_template(
            'pages/user_results.html',
            title='Results'
        )
