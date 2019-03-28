from flask import jsonify
from datetime import datetime
from web import db


class TeacherAnalyticsUtils:
    @staticmethod
    def get_five_years_plan():
        sql = """
        SELECT personnel_number, surname, name, middle_name, qualification_category, rank, previous_attestation_date, 
        next_attestation_date
        FROM teacher;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])

    @staticmethod
    def count_subjects_teachers():
        sql = """
        SELECT subject.subject_name, COUNT(teacher_subject.personnel_number)
        FROM subject
        LEFT OUTER JOIN teacher_subject ON subject.subject_id = teacher_subject.subject_id
        GROUP BY subject.subject_name;
        """
        result = db.engine.execute(sql)
        return jsonify([dict(row) for row in result])

    @staticmethod
    def get_teachers_all_subjects_of_department(filters):
        department = filters.get("department")
        sql = """
        SELECT teacher.personnel_number, teacher.surname
        FROM teacher
        WHERE NOT EXISTS (SELECT *
                            FROM subject
                            WHERE subject.department=%s 
                            AND NOT EXISTS (SELECT *
                                            FROM teacher_subject
                                            WHERE teacher_subject.subject_id=subject.subject_id
                                            AND teacher_subject.personnel_number=teacher.personnel_number));
        """
        result = db.engine.execute(sql, (department,))
        return jsonify([dict(row) for row in result])

    @staticmethod
    def get_teachers_current_year_attestation():
        current_year = datetime.now().year if datetime.now().month < 5 else datetime.now().year + 1
        sql = """
        SELECT *
        FROM teacher
        WHERE next_attestation_date=%s;
        """
        result = db.engine.execute(sql, (current_year,))
        return jsonify([dict(row) for row in result])
