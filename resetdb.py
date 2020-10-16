"""Script for resetting the tables of a database.

First all the tables are dropped, then new tables are created as specified in
`models.py`.

Execute this script by typing in:
    `python resetdb.py`
"""

from clubmatcher import create_app, db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
