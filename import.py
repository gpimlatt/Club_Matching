"""Script for creating/updating club accounts from a JSON file.

When executing this script you must provide a name of a JSON file which
contains the club information. This file must be stored inside of
`Club_Matcher/data/` prior to executing the command. Otherwise, a FileNotFound
error will occur.

How to execute this script:
`python import.py filename.json`

(Where filename.json is `Club_Matcher/data/filename.json` and stores the club
data.)
"""

import sys
import json
from clubmatcher import create_app, db, bcrypt
from clubmatcher.main.models import Club, Tag


def add_club(clubs):
    """Add new clubs to the database or update existing clubs.

    Args:
        clubs:

    Returns:
        True if clubs have been successfully created/updated.
        False otherwise.

    Raises:
        ValueError: An error occured querying the database for
    """
    for club in club_data:
        existing_club = Club.query.get(int(row['SKU']))
        tag = Tag.query.filter_by(name=row['Tags']).first()
        if not existing_tag:
            tag = Tag(name=row['Tags'])
            db.session.add(tag)
        if existing_club:
            existing_club.name = row['Name']
            existing_club.email = row['Email']
            existing_club.description = row['Short description']
            existing_club.ecommerce = row['Storefront Link']
            existing_club.western_link = row['WL Address']
            existing_club.tag = tag
        else:
            hashed_password = bcrypt.generate_password_hash(
                password
            ).decode('utf-8')
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
    return True


def main():
    """Opens file passed in as arg and converts data to dictionary of clubs.

    Returns:
        None
    """
    try:
        with open("data/" + sys.argv[1]) as file:
            clubs = json.load(file)
        is_uploaded = add_club(clubs)
        if is_uploaded:
            print("Clubs uploaded successfully.")
    except IndexError as indexerror:
        print(
            f"""
    IndexError: {indexerror}

    This script requires a JSON file holding club data.
    (JSON file needs to be stored inside `Club_Matcher/data`)
        `python import.py filename.json`

    (The above command will upload events stored in `Club_Matcher/data/filename.json)
"""
        )
    except FileNotFoundError as filenotfound:
        print("Error: File not found.")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
