from numpy import dot
from numpy.linalg import norm


def cosine_similarity(student_answers, club_answers):
    return dot(student_answers, club_answers) / (norm(student_answers) * norm(club_answers))
