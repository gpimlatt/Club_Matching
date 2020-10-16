"""Script for deleting all the tables of a database.

Execute this script by typing in:
    `python deletedb.py`
"""

from clubmatcher import create_app, db

app = create_app()
with app.app_context():
    db.drop_all()
