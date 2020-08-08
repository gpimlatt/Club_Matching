from clubmatcher.models import Club

all_clubs = Club.query.all()
for club in all_clubs:
    print(club)
