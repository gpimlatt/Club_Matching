from numpy import dot
from numpy.linalg import norm
from clubmatcher import db
from clubmatcher.main.models import Statistic


def cosine_similarity(student_answers, club_answers):
    """Computes the cosine similarity between the student and club answers.

    Args:
        student_answers: List of answers provided by the student (i.e. user).
        club_answers: List of answers provided by a club admin.

    Returns:
        Cosine similarity between the two lists.
    """
    return dot(student_answers, club_answers) / (norm(student_answers) * norm(club_answers))


def update_quiz_counter():
    """Increments the quiz submission counter in the Statistic table by one.

    Returns:
        None
    """
    statistic = Statistic.query.get(1)
    statistic.user_quiz_submissions += 1
    db.session.commit()
