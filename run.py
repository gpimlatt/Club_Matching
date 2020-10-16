"""Script for running the Flask application.

Execute this script by typing in:
    `python run.py`
"""

from clubmatcher import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
