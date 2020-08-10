from flask import url_for
from flask_mail import Message
from clubmatcher import mail, create_app
from clubmatcher.main.models import Club


def send_email(recipient):
    message = Message(
        'USC Club Matcher Quiz',
        sender='noreply.westernusc.timeline@gmail.com',
        recipients=[recipient.email]
    )
    message.body = f"""
Dear {recipient.name},

Please follow these instructions to register your club in USC Club Matcher:

1) Login to your account.

    Email: {recipient.email}
    Password: 111222333

2) Take the quiz.

3) Edit any account info.

Click the following link to begin: {url_for('main.login', _external=True)}
"""
    mail.send(message)

app = create_app()
if __name__ == '__main__':
    with app.app_context():
        all_clubs = Club.query.all()
        for club in all_clubs:
            send_email(club)
