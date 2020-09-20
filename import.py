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


def update_ecommerce(filepath):
    with open(filepath) as file:
        club_data = json.load(file)
    for row in club_data:
        club = Club.query.get(int(row['SKU']))
        if club:
            if not club.ecommerce:
                club.ecommerce = row['Storefront Link']
    db.session.commit()


def update_clubs(filepath):
    with open('etc/config.json') as file:
        config = json.load(file)
    password = config.get('USC_CLUB_MATCHER_PASSWORD')
    with open(filepath) as file:
        club_data = json.load(file)
    for row in club_data:
        club = Club.query.get(int(row['SKU']))
        tag = Tag.query.filter_by(name=row['Tags']).first()
        if not tag:
            tag = Tag(name=row['Tags'])
            db.session.add(tag)
        if club:
            club.name = row['Name']
            club.email = row['Email']
            club.description = row['Short description']
            club.ecommerce = row['Storefront Link']
            club.western_link = row['WL Address']
            club.tag = tag
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_club = Club(
                id=row['SKU'],
                name=row['Name'],
                email=row['Email'],
                password=hashed_password,
                description=row['Short description'],
                ecommerce=row['Storefront Link'],
                western_link=row['WL Address'],
                tag=tag
            )
            db.session.add(new_club)
    db.session.commit()


app = create_app()
if __name__ == '__main__':
    with app.app_context():
        update_clubs('data/clubs_updated.json')
