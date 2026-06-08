from collections import defaultdict

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.main import main_bp
from app.main.forms import StudySessionForm
from app.models import StudySession, Subject


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = StudySessionForm()
    subjects = Subject.query.order_by(Subject.group_name, Subject.name).all()
    form.subject_id.choices = [(s.id, f"{s.group_name} — {s.name}") for s in subjects]

    if form.validate_on_submit():
        session = StudySession(
            user_id=current_user.id,
            subject_id=form.subject_id.data,
            hours=form.hours.data,
            notes=form.notes.data or None,
            studied_on=form.studied_on.data,
        )
        db.session.add(session)
        db.session.commit()
        flash("Study session logged successfully!", "success")
        return redirect(url_for("main.dashboard"))

    sessions = (
        StudySession.query.filter_by(user_id=current_user.id)
        .order_by(StudySession.studied_on.desc(), StudySession.created_at.desc())
        .limit(10)
        .all()
    )

    total_hours = (
        db.session.query(db.func.sum(StudySession.hours))
        .filter(StudySession.user_id == current_user.id)
        .scalar()
        or 0
    )

    subject_hours = defaultdict(float)
    for session in StudySession.query.filter_by(user_id=current_user.id).all():
        subject_hours[session.subject.name] += session.hours

    return render_template(
        "main/dashboard.html",
        form=form,
        sessions=sessions,
        total_hours=round(total_hours, 1),
        subject_hours=dict(subject_hours),
        subjects=subjects,
    )
