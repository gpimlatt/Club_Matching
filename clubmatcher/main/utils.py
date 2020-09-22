from numpy import dot
from numpy.linalg import norm
from clubmatcher import db
from clubmatcher.main.models import Statistic


def cosine_similarity(student_answers, club_answers):
    return dot(student_answers, club_answers) / (norm(student_answers) * norm(club_answers))


def update_quiz_counter():
    statistic = Statistic.query.get(1)
    statistic.user_quiz_submissions += 1
    db.session.commit()
