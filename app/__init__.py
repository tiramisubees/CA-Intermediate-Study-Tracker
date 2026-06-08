from flask import Flask

from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.auth import auth_bp
        from app.main import main_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        db.create_all()
        _seed_subjects()

    return app


CANONICAL_SUBJECTS = [
    ("Group 1", "Advanced Accounting"),
    ("Group 1", "Corporate and Other Laws"),
    ("Group 1", "Taxation"),
    ("Group 2", "Cost and Management Accounting"),
    ("Group 2", "Auditing and Ethics"),
    ("Group 2", "Financial Management and Strategic Management"),
]

# Maps retired syllabus entries to their current ICAI replacements.
LEGACY_SUBJECT_MIGRATIONS = {
    ("Group 2", "Auditing and Assurance"): ("Group 2", "Auditing and Ethics"),
    ("Group 1", "Cost and Management Accounting"): ("Group 2", "Cost and Management Accounting"),
    ("Group 2", "Financial Management"): ("Group 2", "Financial Management and Strategic Management"),
    ("Group 2", "Strategic Management"): ("Group 2", "Financial Management and Strategic Management"),
}


def _seed_subjects():
    """Sync the database with the current ICAI Intermediate syllabus."""
    from app.models import StudySession, Subject

    canonical_keys = set(CANONICAL_SUBJECTS)
    subjects_by_key = {(s.group_name, s.name): s for s in Subject.query.all()}

    for group_name, name in CANONICAL_SUBJECTS:
        if (group_name, name) not in subjects_by_key:
            subject = Subject(group_name=group_name, name=name)
            db.session.add(subject)
            subjects_by_key[(group_name, name)] = subject

    db.session.flush()

    for old_key, new_key in LEGACY_SUBJECT_MIGRATIONS.items():
        old_subject = subjects_by_key.get(old_key)
        if not old_subject:
            continue

        new_subject = subjects_by_key.get(new_key)
        if new_subject and new_subject.id != old_subject.id:
            StudySession.query.filter_by(subject_id=old_subject.id).update(
                {"subject_id": new_subject.id}
            )
            db.session.delete(old_subject)
            del subjects_by_key[old_key]

    db.session.flush()

    for (group_name, name), subject in list(subjects_by_key.items()):
        if (group_name, name) not in canonical_keys:
            StudySession.query.filter_by(subject_id=subject.id).delete()
            db.session.delete(subject)

    db.session.commit()
