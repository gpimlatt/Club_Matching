from flask import current_app
from clubmatcher import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Club.query.get(int(user_id))


class Club(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text)
    ecommerce = db.Column(db.Text, nullable=False, default='https://www.westernusc.store/club-memberships/')
    facebook = db.Column(db.Text)
    instagram = db.Column(db.Text)
    twitter = db.Column(db.Text)
    website = db.Column(db.Text)
    western_link = db.Column(db.Text)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    answers = db.Column(db.String(60), nullable=False, default='')

    def __repr__(self):
        return f"Club(name='{self.name}', answers=[{self.answers}])"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    clubs = db.relationship('Club', backref='tag', lazy=True)

    def __repr__(self):
        return f"Tag(name={self.name})"


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_submissions = db.Column(db.Integer)

    def __repr__(self):
        return f"Quiz Submissions: {self.submissions}"
