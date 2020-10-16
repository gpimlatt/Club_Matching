"""Script for creating all the database tables specified in `models.py`.

Execute this script by typing in:
    `python createdb.py`
"""

from clubmatcher import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
