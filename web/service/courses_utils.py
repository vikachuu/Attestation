from datetime import datetime

from web import db
from web.model.courses_models import ReferralToCourses, SelectiveCourseDate


class CoursesUtils:
    @staticmethod
    def create_referral_to_courses(data):
        referral = ReferralToCourses.query.filter_by(personnel_number=data.get('personnel_number'),
                                                     sertificate=False).first()
        if not referral:
            referral = ReferralToCourses(
                referral_number=data.get('referral_number'),
                proff_course_start_date=data.get('proff_course_start_date'),
                proff_course_end_date=data.get('proff_course_end_date'),
                sertificate=data.get('sertificate'),

                personnel_number=data.get('personnel_number')
            )

            db.session.add(referral)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully created referral.'
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Unsertificated referral to course already exists.',
            }
            return response_object, 202

    @staticmethod
    def update_referral_to_courses_by_id(update, referral_id):
        proff_course_start_date = datetime.strptime(update.get('proff_course_start_date'), '%Y-%m-%d').date()
        proff_course_end_date = datetime.strptime(update.get('proff_course_end_date'), '%Y-%m-%d').date()

        sql = """
        UPDATE referral_to_courses
        SET referral_number=%s, proff_course_start_date=%s, proff_course_end_date=%s, sertificate=%s, 
        personnel_number=%s
        WHERE referral_number=%s;
        """
        update_with = (update.get('referral_number'), proff_course_start_date, proff_course_end_date,
                       update.get('sertificate'), update.get('personnel_number'),
                       referral_id)
        db.engine.execute(sql, update_with)
        return {"message": "successfully updated"}

    @staticmethod
    def delete_referral_to_courses_by_id(referral_id):
        sql = """
        DELETE FROM referral_to_courses
        WHERE referral_number=%s;
        """
        db.engine.execute(sql, (referral_id,))
        return {"message": "successfully deleted referral"}

    @staticmethod
    def create_date_of_course(data):
        selective_course_date = SelectiveCourseDate(
            date_of_course=data.get('date_of_course'),
            referral_number=data.get('referral_number')
        )

        db.session.add(selective_course_date)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully created date of course.'
        }
        return response_object, 200
