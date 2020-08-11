import os
import json
from clubmatcher import create_app, db, bcrypt
from clubmatcher.main.models import Club, Tag

password = os.environ.get('USC_CLUB_MATCHER_PASSWORD')
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


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


def import_generic_clubs():
    club_1 = Club(
        name='Club One',
        email='noreply.westernusc.timeline+1@gmail.com',
        password=hashed_password
    )

    club_2 = Club(
        name='Club Two',
        email='noreply.westernusc.timeline+2@gmail.com',
        password=hashed_password
    )

    club_3 = Club(
        name='Club Three',
        email='noreply.westernusc.timeline+3@gmail.com',
        password=hashed_password
    )
    db.session.add(club_1)
    db.session.add(club_2)
    db.session.add(club_3)
    db.session.commit()


app = create_app()
if __name__ == '__main__':
    with app.app_context():
        import_generic_clubs()
        # import_tags('data/tags.json')
        # import_clubs('data/clubs-2.json')
