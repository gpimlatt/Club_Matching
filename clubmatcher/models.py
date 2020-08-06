from clubmatcher import db


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ecommerce = db.Column(db.Text, nullable=False, default='https://www.westernusc.store/club-memberships/')
    facebook = db.Column(db.Text)
    instagram = db.Column(db.Text)
    twitter = db.Column(db.Text)
    website = db.Column(db.Text)
    answers = db.Column(db.String(60), nullable=False, default='')

    def __repr__(self):
        return f"Club(name='{self.name}', answers=[{self.answers}])"
