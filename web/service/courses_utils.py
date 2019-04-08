from datetime import datetime

from flask import jsonify

from web import db
from web.model.courses_models import ReferralToCourses, SelectiveCourseDate


class CoursesUtils:
    @staticmethod
    def create_referral_to_courses(data):
        referral = ReferralToCourses.query.filter_by(referral_number=data.get('referral_number')).first()
        if referral:
            response_object = {
                'status': 'fail',
                'message': 'Referral with such referral number exists.'
            }
            return response_object, 400
        referral = ReferralToCourses.query.filter_by(personnel_number=data.get('personnel_number'),
                                                     sertificate=False).first()
        # TODO: check if teacher exists
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
    def create_date_of_course(data, referral_number):
        selective_course_date = SelectiveCourseDate(
            date_of_course=data.get('date_of_course'),
            referral_number=referral_number
        )

        db.session.add(selective_course_date)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully created date of course.'
        }
        return response_object, 200

    @staticmethod
    def update_date_of_course(update, course_id, referral_number):
        date_of_course = datetime.strptime(update.get('date_of_course'), '%Y-%m-%d').date()

        sql = """
        UPDATE selective_course_date
        SET date_of_course=%s, referral_number=%s
        WHERE date_of_course_id=%s;
        """
        update_with = (date_of_course, referral_number, course_id)
        db.engine.execute(sql, update_with)
        return {"message": "successfully updated date of course"}

    @staticmethod
    def get_all_teachers_with_courses():
        sql = """
        SELECT T.personnel_number, T.surname, T.name, T.middle_name, C.referral_number, C.proff_course_start_date, 
        C.proff_course_end_date, C.sertificate, C.selective_courses
        FROM teacher AS T
        RIGHT OUTER JOIN (SELECT R.referral_number, R.proff_course_start_date, R.proff_course_end_date, R.sertificate, 
                                R.personnel_number,
                                CASE WHEN COUNT(R.referral_number) = 0 THEN ARRAY[]::json[] ELSE
                                array_agg(json_build_object('date_of_course_id', S.date_of_course_id, 
                                'date_of_course', S.date_of_course)) END AS selective_courses
                          FROM referral_to_courses AS R
                          LEFT OUTER JOIN selective_course_date AS S ON R.referral_number = S.referral_number
                          GROUP BY R.referral_number, R.proff_course_start_date, R.proff_course_end_date, 
                                   R.sertificate) AS C

        ON T.personnel_number = C.personnel_number;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])

    @staticmethod
    def get_all_teachers_of_subject_with_courses(filters):
        subject = filters.get('subject')
        sql = """
            SELECT T.personnel_number, T.surname, T.name, T.middle_name, C.referral_number, C.proff_course_start_date, 
            C.proff_course_end_date, C.sertificate, C.selective_courses,
            CASE WHEN COUNT(S.subject_id) = 0 THEN ARRAY[]::json[] ELSE
            array_agg(json_build_object('subject_id', S.subject_id, 'department', S.department, 
                        'subject_name', S.subject_name)) END AS subjects
            FROM teacher AS T
            RIGHT OUTER JOIN (SELECT R.referral_number, R.proff_course_start_date, R.proff_course_end_date, R.sertificate, 
                                    R.personnel_number,
                                    CASE WHEN COUNT(R.referral_number) = 0 THEN ARRAY[]::jsonb[] ELSE
                                    array_agg(jsonb_build_object('date_of_course_id', S.date_of_course_id, 
                                    'date_of_course', S.date_of_course)) END AS selective_courses
                              FROM referral_to_courses AS R
                              LEFT OUTER JOIN selective_course_date AS S ON R.referral_number = S.referral_number
                              GROUP BY R.referral_number, R.proff_course_start_date, R.proff_course_end_date, 
                                       R.sertificate) AS C

            ON T.personnel_number = C.personnel_number
            
            LEFT OUTER JOIN teacher_subject AS TS ON T.personnel_number = TS.personnel_number
            LEFT OUTER JOIN subject AS S ON S.subject_id = TS.subject_id
            
            WHERE (%s IS NULL OR  EXISTS (SELECT *
                                            FROM teacher AS T2
                                            LEFT OUTER JOIN teacher_subject AS TS2 ON T2.personnel_number = TS2.personnel_number
                                            LEFT OUTER JOIN subject AS S2 ON S2.subject_id = TS2.subject_id
                                            WHERE TS2.personnel_number=T.personnel_number AND S2.subject_name=%s))
            GROUP BY T.personnel_number, T.surname, T.name, T.middle_name, C.referral_number, C.proff_course_start_date, 
                        C.proff_course_end_date, C.sertificate, C.selective_courses;
            """
        result = db.engine.execute(sql, (subject, subject))
        return jsonify([dict(row) for row in result])
