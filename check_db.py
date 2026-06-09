from app import create_app
from app.models import User, Subject, StudySession

app = create_app()

with app.app_context():
    print("Users:", User.query.count())
    print("Subjects:", Subject.query.count())
    print("Study Sessions:", StudySession.query.count())