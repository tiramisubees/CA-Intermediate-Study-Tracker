from app import create_app
from app.models import Chapter

app = create_app()

with app.app_context():
    print("Chapter count:", Chapter.query.count())