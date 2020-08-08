import os
import json
from clubmatcher import db, bcrypt
from clubmatcher.models import Club, Tag

password = os.environ.get('USC_CLUB_MATCHER_PASSWORD')
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

community_tag = Tag.query.get(1)
philanthropy_tag = Tag.query.get(2)
hobbies_tag = Tag.query.get(3)
health_tag = Tag.query.get(4)
cultural_tag = Tag.query.get(5)


def import_tags(filepath):
    with open(filepath) as file:
        tags = json.load(file)
    for tag in tags:
        if not Tag.query.filter_by(name=tag['Name']).first():
            db.session.add(Tag(name=tag['Name']))
    db.session.commit()


def import_clubs(filepath):
    with open(filepath) as file:
        clubs = json.load(file)
    for club in clubs:
        pass


if __name__ == '__main__':
    import_tags('data/tags.json.json')
