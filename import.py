import os
import json
import re
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


def add_ecommerce_url_and_description(filepath):
    with open(filepath) as file:
        clubs = json.load(file)
    for club_data in clubs:
        club = Club.query.get(club_data['SKU'])
        if club:
            club.ecommerce = club_data['StoreURL']
            club.description = club_data['Short description']
            db.session.commit()


def import_clubs(filepath):
    with open('etc/config.json') as file:
        config = json.load(file)
    password = config.get('USC_CLUB_MATCHER_PASSWORD')
    with open(filepath) as file:
        clubs = json.load(file)
    for club in clubs:
        if club['Organization Email']:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_club = Club(
                id=club['Organization ID'],
                name=club['Organization Name'],
                email=club['Organization Email'],
                password=hashed_password
            )
            db.session.add(new_club)
    db.session.commit()


app = create_app()
if __name__ == '__main__':
    with app.app_context():
        # import_tags('data/tags.json')
        # import_clubs('data/clubs-2.json')
        add_ecommerce_url_and_description('data/club_ecommerce.json')
