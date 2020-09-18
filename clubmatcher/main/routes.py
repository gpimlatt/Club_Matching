from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from clubmatcher import db, bcrypt, mail
from clubmatcher.main.forms import UpdateClubForm, QuizForm, LoginForm
from clubmatcher.main.models import Club
from clubmatcher.main.utils import cosine_similarity

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.answers:
            return redirect(url_for('main.account'))
        else:
            return redirect(url_for('main.quiz'))
    form = LoginForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        if club and bcrypt.check_password_hash(club.password, form.password.data):
            login_user(club)
            if club.answers:
                return redirect(url_for('main.account'))
            else:
                return redirect(url_for('main.quiz'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'error')
    return render_template(
        'pages/login.html',
        title='Login',
        form=form
    )


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateClubForm()
    quiz_completed = True if current_user.answers else False
    if form.validate_on_submit():
        current_user.ecommerce = form.ecommerce.data
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        current_user.twitter = form.twitter.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your club information has been updated!', 'success')
    elif request.method == 'GET':
        form.ecommerce.data = current_user.ecommerce
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram
        form.twitter.data = current_user.twitter
        form.website.data = current_user.website
    return render_template(
        'pages/update_account.html',
        title='Update Club Information',
        form=form,
        quiz_completed=quiz_completed
    )


@main.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )


@main.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        flash("You must complete the quiz first.", "error")
        return redirect(url_for('main.quiz'))
    elif QuizForm(request.form).validate_on_submit():
        form = QuizForm(request.form)
        q1 = form.q1_field.data[1:-1].split(',')
        q2 = form.q2_field.data[1:-1].split(',')
        q3 = form.q3_field.data
        q4 = form.q4_field.data
        q5 = form.q5_field.data
        q6 = form.q6_field.data
        q7 = form.q7_field.data
        q8 = form.q8_field.data
        q9 = form.q9_field.data
        q10 = form.q10_field.data[1:-1].split(',')
        if current_user.is_authenticated:
            club_answers = ''.join(q1).replace(' ', ',') + ',' + \
                           ''.join(q2).replace(' ', ',') + ',' + \
                           q3 + ',' + q4 + ',' + q5 + ',' + q6 + ',' + q7 + ',' + q8 + ',' + q9 + ',' + \
                           ''.join(q10).replace(' ', ',')
            current_user.answers = club_answers
            db.session.commit()
            flash('Thank you, your answers have been recorded!', 'success')
            return redirect(url_for('main.account'))
        else:
            student_answers = q1 + q2
            student_answers.extend([q3, q4, q5, q6, q7, q8, q9])
            student_answers = student_answers + q10
            student_answers = [int(answer) for answer in student_answers]
            recommended_club_ids = {}
            clubs = Club.query.all()
            for club in clubs:
                if club.answers:
                    club_answers = club.answers.split(',')
                    club_answers = [int(answer) for answer in club_answers]
                    similarity_score = cosine_similarity(student_answers, club_answers)
                    if len(recommended_club_ids) < 3:
                        recommended_club_ids[club.id] = similarity_score
                        recommended_club_ids = {k: v for k, v in sorted(
                            recommended_club_ids.items(),
                            key=lambda item: item[1]
                        )}
                    else:
                        for club_id in list(recommended_club_ids):
                            if recommended_club_ids[club_id] < similarity_score:
                                del recommended_club_ids[club_id]
                                recommended_club_ids[club.id] = similarity_score
                                recommended_club_ids = {k: v for k, v in sorted(
                                    recommended_club_ids.items(),
                                    key=lambda item: item[1]
                                )}
                                break
            recommended_clubs = []
            recommended_club_ids = {k: v for k, v in sorted(
                recommended_club_ids.items(),
                key=lambda item: item[1],
                reverse=True
            )}
            for id in recommended_club_ids:
                recommended_clubs.append(Club.query.get(id))
            return render_template(
                'pages/user_results.html',
                title='Results',
                recommended_clubs=recommended_clubs,
            )
    else:
        form = QuizForm()
        flash('Please answer all quiz questions.', 'error')
        return render_template(
            'pages/quiz.html',
            title='Quiz',
            form=form
        )
