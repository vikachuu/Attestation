from datetime import datetime

from flask import jsonify
from web import db
from web.model.teacher_model import Teacher, CATEGORY, RANK
from web.service.utils import requires_access_level


class TeacherUtils:

    @staticmethod
    @requires_access_level(2)
    def create_teacher(data, token):
        teacher = Teacher.query.filter_by(personnel_number=data.get('personnel_number')).first()
        if not teacher:
                teacher = Teacher(
                    personnel_number=data.get('personnel_number'),
                    employment_history=data.get('employment_history'),
                    surname=data.get('surname'),
                    name=data.get('name'),
                    middle_name=data.get('middle_name'),
                    birth_date=data.get('birth_date'),

                    educational_institution=data.get('educational_institution'),
                    specialty=data.get('specialty'),
                    accreditation_level=data.get('accreditation_level'),
                    graduation_year=data.get('graduation_year'),
                    position=data.get('position'),
                    experience=data.get('experience'),

                    qualification_category=data.get('qualification_category'),
                    rank=data.get('rank'),
                    previous_attestation_date=data.get('previous_attestation_date'),
                    next_attestation_date=data.get('next_attestation_date'),
                    degree=data.get('degree'),
                    avatar_url=data.get('avatar_url')
                )

                # insert the user
                db.session.add(teacher)  # TODO: insert teacher to table sql query
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created teacher {}.'.format(teacher.surname)
                }
                return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Teacher already exists.',
            }
            return response_object, 202

    @staticmethod
    def get_teacher_by_id(personnel_number):
        sql = """
        SELECT teacher.personnel_number, teacher.employment_history, teacher.surname, teacher.name, teacher.middle_name,
        teacher.birth_date, teacher.educational_institution, teacher.specialty, teacher.accreditation_level, 
        teacher.graduation_year, teacher.position, teacher.experience, teacher.qualification_category, teacher.rank,
        teacher.previous_attestation_date, teacher.next_attestation_date, teacher.degree, teacher.avatar_url,
        
        CASE WHEN COUNT(subject.subject_id) = 0 THEN ARRAY[]::json[] ELSE
        array_agg(json_build_object('subject_id', subject.subject_id, 
                'department', subject.department, 'subject_name', subject.subject_name)) END AS subjects
        FROM teacher 
        LEFT OUTER JOIN teacher_subject ON teacher.personnel_number = teacher_subject.personnel_number
        LEFT OUTER JOIN subject ON subject.subject_id = teacher_subject.subject_id
        WHERE teacher.personnel_number=%s
        GROUP BY teacher.personnel_number, teacher.employment_history, teacher.surname, teacher.name, teacher.middle_name,
        teacher.birth_date, teacher.educational_institution, teacher.specialty, teacher.accreditation_level, 
        teacher.graduation_year, teacher.position, teacher.experience, teacher.qualification_category, teacher.rank,
        teacher.previous_attestation_date, teacher.next_attestation_date, teacher.degree, teacher.avatar_url;
        """
        result = db.engine.execute(sql, (personnel_number,))
        teacher = [dict(row) for row in result]
        if teacher:
            return jsonify(teacher[0])
        else:
            response_object = {
                'status': 'fail',
                'message': 'No teacher exists with such id.',
            }
            return response_object

    @staticmethod
    def get_teacher_by_id_with_courses(personnel_number):
        sql = """
        SELECT T.personnel_number, T.employment_history, T.surname, T.name, T.middle_name, T.birth_date, 
        T.educational_institution, T.specialty, T.accreditation_level, T.graduation_year, T.position, T.experience, 
        T.qualification_category, T.rank, T.previous_attestation_date, T.next_attestation_date, T.degree, T.avatar_url, 
        C.referral_number, C.proff_course_start_date, C.proff_course_end_date, C.sertificate, C.selective_courses,
        CASE WHEN COUNT(S.subject_id) = 0 THEN ARRAY[]::json[] ELSE
        array_agg(json_build_object('subject_id', S.subject_id, 'department', S.department, 
                    'subject_name', S.subject_name)) END AS subjects
        FROM teacher AS T
        LEFT OUTER JOIN (SELECT R.referral_number, R.proff_course_start_date, R.proff_course_end_date, R.sertificate, 
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

        WHERE T.personnel_number=%s
        GROUP BY T.personnel_number, T.employment_history, T.surname, T.name, T.middle_name, T.birth_date, 
        T.educational_institution, T.specialty, T.accreditation_level, T.graduation_year, T.position, T.experience, 
        T.qualification_category, T.rank, T.previous_attestation_date, T.next_attestation_date, T.degree, T.avatar_url, 
        C.referral_number, C.proff_course_start_date, C.proff_course_end_date, C.sertificate, C.selective_courses
        ORDER BY proff_course_start_date DESC
        LIMIT 1;
        """
        result = db.engine.execute(sql, (personnel_number,))
        teacher = [dict(row) for row in result]
        if teacher:
            return jsonify(teacher[0])
        else:
            response_object = {
                'status': 'fail',
                'message': 'No teacher exists with such id.',
            }
            return response_object

    @staticmethod
    def delete_teacher_by_id(personnel_number):
        sql = """
        DELETE FROM teacher
        WHERE personnel_number=%s;
        """
        db.engine.execute(sql, (personnel_number, ))
        return {"message": "successfully deleted"}

    @staticmethod
    def update_teacher_by_id(personnel_number, update):
        sql = """
        UPDATE teacher
        SET personnel_number=%s, employment_history=%s, surname=%s, name=%s, middle_name=%s, birth_date=%s,
                 educational_institution=%s, specialty=%s, accreditation_level=%s, graduation_year=%s, position=%s, 
                 experience=%s, qualification_category=%s, rank=%s, previous_attestation_date=%s, 
                 next_attestation_date=%s, degree=%s, avatar_url=%s
        WHERE personnel_number=%s;
        """
        qualification_category = update.get('qualification_category')
        rank = update.get('rank')
        birth_date = datetime.strptime(update.get('birth_date'), '%Y-%m-%d').date()

        update_with = (update.get('personnel_number'), update.get('employment_history'), update.get('surname'),
                       update.get('name'), update.get('middle_name'), birth_date,
                       update.get('educational_institution'), update.get('specialty'),
                       update.get('accreditation_level'), update.get('graduation_year', None), update.get('position'),
                       update.get('experience'),
                       CATEGORY[qualification_category].value,
                       RANK[rank].value if rank else None,
                       update.get('previous_attestation_date'), update.get('next_attestation_date'),
                       update.get('degree', None), update.get('avatar_url', None),
                       personnel_number)
        db.engine.execute(sql, update_with)
        return {"message": "successfully updated"}

    @staticmethod
    def get_all_teachers():
        sql = """
        SELECT teacher.personnel_number, teacher.surname, teacher.name, teacher.qualification_category, teacher.rank,
        CASE WHEN COUNT(subject.subject_id) = 0 THEN ARRAY[]::json[] ELSE
        array_agg(json_build_object('subject_id', subject.subject_id, 
                'department', subject.department, 'subject_name', subject.subject_name)) END AS subjects
        FROM teacher 
        LEFT OUTER JOIN teacher_subject ON teacher.personnel_number = teacher_subject.personnel_number
        LEFT OUTER JOIN subject ON subject.subject_id = teacher_subject.subject_id
        GROUP BY teacher.personnel_number, teacher.surname, teacher.name, teacher.qualification_category, teacher.rank;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])

    @staticmethod
    def get_filtered_teachers(filters):
        qualification_category = filters.get("qualification_category")
        rank = filters.get("rank")
        subject_name = filters.get("subject_name")

        sql = """        
        SELECT teacher.personnel_number, teacher.surname, teacher.name, teacher.qualification_category, teacher.rank,
        CASE WHEN COUNT(subject.subject_id) = 0 THEN ARRAY[]::json[] ELSE
        array_agg(json_build_object('subject_id', subject.subject_id, 
                'department', subject.department, 'subject_name', subject.subject_name)) END AS subjects
        FROM teacher 
        LEFT OUTER JOIN teacher_subject ON teacher.personnel_number = teacher_subject.personnel_number
        LEFT OUTER JOIN subject ON subject.subject_id = teacher_subject.subject_id
        
        WHERE (%s IS NULL OR teacher.qualification_category=%s)
        AND (%s IS NULL OR teacher.rank=%s)
        AND (%s IS NULL OR  EXISTS (SELECT *
                                    FROM teacher AS T2
                                    LEFT OUTER JOIN teacher_subject AS TS2 ON T2.personnel_number = TS2.personnel_number
                                    LEFT OUTER JOIN subject AS S2 ON S2.subject_id = TS2.subject_id
                                    WHERE TS2.personnel_number=teacher.personnel_number AND S2.subject_name=%s))
        GROUP BY teacher.personnel_number, teacher.surname, teacher.name, teacher.qualification_category, teacher.rank;
        """
        result = db.engine.execute(sql, (qualification_category, qualification_category,  rank, rank, subject_name, subject_name))
        return jsonify([dict(row) for row in result])

    @staticmethod
    def if_teacher_exists(personnel_number):
        sql = """
        SELECT *
        FROM teacher
        WHERE personnel_number=%s;
        """
        result = db.engine.execute(sql, (personnel_number,))
        teacher = [dict(row) for row in result]
        return True if teacher else False

    @staticmethod
    def get_category_by_personnel_number(personnel_number):
        sql = """
        SELECT qualification_category
        FROM teacher
        WHERE personnel_number=%s;
        """
        result = db.engine.execute(sql, (personnel_number,))
        return result.fetchall()[0][0]

    @staticmethod
    def get_rank_by_personnel_number(personnel_number):
        sql = """
        SELECT rank
        FROM teacher
        WHERE personnel_number=%s;
        """
        result = db.engine.execute(sql, (personnel_number,))
        return result.fetchall()[0][0]

    @staticmethod
    def get_next_attestation_date_by_id(personnel_number):
        sql = """
        SELECT next_attestation_date
        FROM teacher
        WHERE personnel_number=%s;
        """
        result = db.engine.execute(sql, (personnel_number,))
        year = [dict(row) for row in result]
        return year[0]["next_attestation_date"]

    @staticmethod
    def update_teacher_next_attestation_year(personnel_number, next_attestation_date):
        sql = """
        UPDATE teacher
        SET next_attestation_date=%s
        WHERE personnel_number=%s;
        """
        db.engine.execute(sql, (next_attestation_date, personnel_number))
        return {"message": "successfully updated"}

    @staticmethod
    def update_teacher_after_attestation(personnel_number, new_category, new_rank, new_prev_date, new_next_date):
        sql = """
        UPDATE teacher
        SET qualification_category=%s, rank=%s, previous_attestation_date=%s, next_attestation_date=%s
        WHERE personnel_number=%s;
        """
        update_with = (CATEGORY[new_category].value, RANK[new_rank].value if new_rank else None, new_prev_date,
                       new_next_date, personnel_number)
        db.engine.execute(sql, update_with)
        return {"message": "successfully updated teacher after attestation"}
