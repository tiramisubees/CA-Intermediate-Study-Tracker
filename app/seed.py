from app import db
from app.models import Subject, Chapter
from app.syllabus import SYLLABUS


def seed_chapters_for_user(user_id):

    existing = Chapter.query.filter_by(user_id=user_id).count()

    if existing > 0:
        return



    for group_name, subjects in SYLLABUS.items():

        for subject_name, subject_data in subjects.items():

            subject = Subject.query.filter_by(
                group_name=group_name,
                name=subject_name
            ).first()

            if not subject:
                continue

            # Normal subjects
            if "Chapters" in subject_data:

                chapter_list = subject_data["Chapters"]

            # Taxation
            elif "Direct Tax" in subject_data:

                chapter_list = (
                    subject_data["Direct Tax"]
                    + subject_data["Indirect Tax"]
                )

            # FM-SM
            elif "Financial Management" in subject_data:

                chapter_list = (
                    subject_data["Financial Management"]
                    + subject_data["Strategic Management"]
                )

            else:
                continue

            for chapter_name in chapter_list:

                chapter = Chapter(
                    user_id=user_id,
                    subject_id=subject.id,
                    name=chapter_name
                )

                db.session.add(chapter)

    db.session.commit()