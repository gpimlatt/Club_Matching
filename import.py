import os
import json
from clubmatcher import create_app, db, bcrypt
from clubmatcher.main.models import Club, Tag


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
    with open('etc/config.json') as file:
        config = json.load(file)
    password = config.get('USC_CLUB_MATCHER_PASSWORD')
    with open(filepath) as file:
        clubs = json.load(file)
    for club in clubs:
        if not Club.query.filter_by(email=club['Email']).first():
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
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


app = create_app()
if __name__ == '__main__':
    with app.app_context():
        import_tags('data/tags.json')
        import_clubs('data/sample-clubs.json')
