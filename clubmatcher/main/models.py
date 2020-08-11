from flask import current_app
from clubmatcher import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Club.query.get(int(user_id))


club_tags = db.Table(
    'club_tags',
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


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
    answers = db.Column(db.String(60), nullable=False, default='')
    quiz_completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Club(name='{self.name}', answers=[{self.answers}])"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    clubs = db.relationship('Club', secondary=club_tags, backref='tags', lazy=True)

    def __repr__(self):
        return f"Tag(name={self.name})"
