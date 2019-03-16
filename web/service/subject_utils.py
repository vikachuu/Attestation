from web import db
from web.model.subject_model import Subject


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
