from flask import jsonify

from web import db
from web.model.extra_app_model import ExtraApplication, STATUS
from web.service.teacher_utils import TeacherUtils


class ExtraApplicationUtils:

    @staticmethod
    def create_extra_application(data):
        extra_application = ExtraApplication.query.\
            filter_by(personnel_number=data.get('personnel_number'),
                      extra_application_status=STATUS['IN_PROGRESS'].value).first()
        if not extra_application:
            personnel_number = data.get('personnel_number')
            if personnel_number and TeacherUtils.if_teacher_exists(personnel_number):
                extra_application = ExtraApplication(
                    extra_application_date=data.get('extra_application_date'),
                    extra_application_reason=data.get('extra_application_reason'),
                    extra_application_status=data.get('extra_application_status'),
                    personnel_number=personnel_number
                )

                db.session.add(extra_application)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created extra application'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'No such teacher for application exists',
                }
                return response_object, 400
        else:
            response_object = {
                'status': 'fail',
                'message': 'You can''t create application while there is one in progress.',
            }
            return response_object, 400

    @staticmethod
    def update_extra_application(application_id, data):
        sql = """
        UPDATE extra_application
        SET extra_application_number=%s, extra_application_date=%s, extra_application_reason=%s, 
        extra_application_status=%s, personnel_number=%s
        WHERE extra_application_number=%s;
        """
        update_with = (data.get('extra_application_number'), data.get('extra_application_date'),
                       data.get('extra_application_reason'), STATUS[data.get('extra_application_status')].value,
                       data.get('personnel_number'), application_id)
        db.engine.execute(sql, update_with)
        return {"message": "successfully updated extra application"}

    @staticmethod
    def get_filtered_extra_applications(filters):
        status = filters.get("status")
        sql = """        
        SELECT *
        FROM extra_application 
        WHERE (%s IS NULL OR extra_application.extra_application_status=%s)
        """
        result = db.engine.execute(sql, (status, status))
        return jsonify([dict(row) for row in result])

    @staticmethod
    def count_filtered_extra_applications(filters):
        status = filters.get("status")
        sql = """        
        SELECT COUNT(*)
        FROM extra_application 
        WHERE (%s IS NULL OR extra_application.extra_application_status=%s)
                """
        result = db.engine.execute(sql, (status, status))
        # return jsonify([dict(row) for row in result])
        return result.scalar()
