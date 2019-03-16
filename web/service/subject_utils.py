from flask import jsonify

from web import db
from web.model.subject_model import Subject, TeacherSubject


class SubjectUtils:
    @staticmethod
    def create_subject(data):
        subject = Subject.query.filter_by(subject_name=data.get('subject_name')).first()
        if not subject:
            subject = Subject(
                subject_name=data.get('subject_name'),
                department=data.get('department')
            )
            # insert the subject
            db.session.add(subject)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully created subject {}.'.format(subject.subject_name)
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Subject already exists.',
            }
            return response_object, 500

    @staticmethod
    def get_all_subjects():
        sql = """
        SELECT *
        FROM subject;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])


class TeacherSubjectUtils:
    @staticmethod
    def create_teacher_subject(data):
        teacher_subject = TeacherSubject.query.filter_by(subject_id=data.get('subject_id'),
                                                         personnel_number=data.get('personnel_number')).first()
        if not teacher_subject:
            teacher_subject = TeacherSubject(
                subject_id=data.get('subject_id'),
                personnel_number=data.get('personnel_number')
            )
            # insert the teacher_subject
            db.session.add(teacher_subject)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully created teacher_subject'
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Teacher_subject already exists.',
            }
            return response_object, 500

    @staticmethod
    def delete_teacher_subject_by_teacher_id(personnel_number):
        sql = """
        DELETE FROM teacher_subject
        WHERE personnel_number=%s;
        """
        db.engine.execute(sql, (personnel_number,))
        return {"message": "successfully deleted"}
