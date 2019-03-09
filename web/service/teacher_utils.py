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
        SELECT *
        FROM teacher
        WHERE personnel_number=%s;
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

        update_with = (update.get('personnel_number'), update.get('employment_history'), update.get('surname'),
                       update.get('name'), update.get('middle_name'), update.get('birth_date'),
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
        SELECT personnel_number, surname, name, qualification_category, rank
        FROM teacher;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])

    @staticmethod
    def get_filtered_teachers(filters):
        qualification_category = filters.get("qualification_category")
        rank = filters.get("rank")

        if qualification_category and rank:
            sql = """
            SELECT personnel_number, surname, name, qualification_category, rank
            FROM teacher
            WHERE qualification_category=%s AND rank=%s;
            """
            result = db.engine.execute(sql, (qualification_category, rank))
        elif qualification_category:
            sql = """
            SELECT *
            FROM teacher
            WHERE qualification_category=%s;
            """
            result = db.engine.execute(sql, (qualification_category,))
        elif rank:
            sql = """
            SELECT *
            FROM teacher
            WHERE rank=%s;
            """
            result = db.engine.execute(sql, (rank,))
        else:
            sql = """
            SELECT *
            FROM teacher;
            """
            result = db.engine.execute(sql)

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
