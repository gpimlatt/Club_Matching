import os
import json
import re
from clubmatcher import create_app, db, bcrypt
from clubmatcher.main.models import Club, Tag


def import_clubs(filepath):
    with open('etc/config.json') as file:
        config = json.load(file)
    password = config.get('USC_CLUB_MATCHER_PASSWORD')
    with open(filepath) as file:
        clubs = json.load(file)
    for club in clubs:
        if club['Email']:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            tag = Tag.query.filter_by(name=club['Tags']).first()
            if not tag:
                tag = Tag(name=club['Tags'])
                db.session.add(tag)
            new_club = Club(
                id=club['SKU'],
                name=club['Name'],
                email=club['Email'],
                password=hashed_password,
                description=club['Short description'],
                ecommerce=club['Storefront Link'],
                western_link=club['WL Address'],
                tag=tag
            )
            db.session.add(new_club)
    db.session.commit()


app = create_app()
if __name__ == '__main__':
    with app.app_context():
        import_clubs('data/clubs.json')
