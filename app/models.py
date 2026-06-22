from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """A registered student who can log study sessions."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    attempt = db.Column(db.String(10), nullable=False, default="SEP26")
    theme = db.Column(db.String(10), default="light", nullable=False)
    exam_attempt = db.Column(db.String(20), default="May")
    daily_goal = db.Column(db.Float, default=4.0)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    study_sessions = db.relationship("StudySession", backref="user", lazy=True)
    chapters = db.relationship("Chapter", backref="user", lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    """A CA Intermediate subject (pre-loaded for all users)."""

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    study_sessions = db.relationship("StudySession", backref="subject", lazy=True)
    chapters = db.relationship("Chapter", backref="subject", lazy=True)

class Chapter(db.Model):
    """Tracks syllabus chapters, AS and SA progress."""

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subject.id"),
        nullable=False
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
class StudySession(db.Model):
    """One study log entry: subject, hours, and optional notes."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    studied_on = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
