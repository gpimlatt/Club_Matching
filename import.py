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


def add_tag_to_db(name):
    if not Tag.query.filter_by(name=name).first():
        db.session.add(Tag(name=name))


def import_tags(filepath):
    with open(filepath) as file:
        tags = json.load(file)
    for tag in tags:
        add_tag_to_db(tag['Name'])
    db.session.commit()


def import_clubs(filepath):
    with open(filepath) as file:
        clubs = json.load(file)
    for club in clubs:
        if not Club.query.filter_by(email=club['Email']).first():
            new_club = Club(
                name=club['Name'],
                email=club['Email'],
                password=hashed_password,
                description=club['Short description'],
                website=club['Website']
            )
            if club['Tags']:
                tags = club['Tags'].split(',')
                for tag in tags:
                    if Tag.query.filter_by(name=tag).first():
                        new_club.tags.append(Tag.query.filter_by(name=tag).first())
                    else:
                        add_tag_to_db(tag)
                        new_club.tags.append(Tag.query.filter_by(name=tag).first())
            db.session.add(new_club)
    db.session.commit()


if __name__ == '__main__':
    import_tags('data/tags.json')
    import_clubs('data/clubs-2.json')
