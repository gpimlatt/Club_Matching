import os
from clubmatcher import db, bcrypt
from clubmatcher.models import Club, Tag

password = os.environ.get('USC_CLUB_MATCHER_PASSWORD')
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


def import_clubs():
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


if __name__ == '__main__':
    import_clubs()
