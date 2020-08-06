from flask import render_template, redirect, url_for
from clubmatcher import app, db, bcrypt
from clubmatcher.forms import ClubForm
from clubmatcher.models import Club


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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        club = Club(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            ecommerce=form.ecommerce.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            twitter=form.twitter.data,
            website=form.website.data
        )
        return redirect(url_for('index'))
    return render_template(
        'pages/register.html',
        title='Register Your Club',
        form=form
    )
