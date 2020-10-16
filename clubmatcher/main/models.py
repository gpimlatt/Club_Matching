from flask import current_app
from clubmatcher import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Retrieves a Club with specific ID from the database.

    Args:
        user_id: Club ID

    Returns:
        An instance of Club with <user_id>, if it exists.
        Otherwise, None.
    """
    return Club.query.get(int(user_id))


class Club(db.Model, UserMixin):
    """Defines a Club table in the database storing various club information.

    Attributes:
        id:
            Primary key for club id.
        name:
            String column for club name.
        email:
            String column for club email.
        password:
            String column for club password.
        description:
            Text column for club description.
        ecommerce:
            Text column for club's Western eCommerce page url.
        facebook:
            Text column for club's Facebook page url.
        instagram:
            Text column for club's Instagram page url.
        twitter:
            Text column for club's Twitter page url.
        website:
            Text column for club's official website url.
        western_link:
            Text column for club's WesternLink page url.
        tag_id:
            Integer column storing the club's tag id (many-to-one relationship
             with Tag table).
        answers:
            String column storing a CSV of the club's quiz answers.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text)
    ecommerce = db.Column(
        db.Text,
        nullable=False,
        default='https://www.westernusc.store/club-memberships/'
    )
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
    """Defines a Tag table in the database.

    Attributes:
        id:
            Primary key for tag id.
        name:
            String column storing tag name.
        clubs:
            Defines one-to-many relationship with Club table.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    clubs = db.relationship('Club', backref='tag', lazy=True)

    def __repr__(self):
        return f"Tag(name={self.name})"


class Statistic(db.Model):
    """Defines a Statistic table in the database.

    Attributes:
        id:
            Primary key.
        user_quiz_submissions:
            Integer column storing number of quiz submissions.

    TODO: Explore better solutions to keep count of quiz submissions.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_quiz_submissions = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Number of Quiz Submissions: {self.user_quiz_submissions}"
