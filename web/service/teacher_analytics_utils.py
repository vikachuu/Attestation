from flask import jsonify

from web import db


class TeacherAnalyticsUtils:
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
