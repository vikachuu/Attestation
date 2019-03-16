from flask import request
from flask_restful import Resource

from web.service.subject_utils import SubjectUtils, TeacherSubjectUtils


class CreateSubject(Resource):
    def post(self):
        data = request.get_json()
        return SubjectUtils.create_subject(data)

    def get(self):
        return SubjectUtils.get_all_subjects()


class CreateTeacherSubject(Resource):
    def post(self):
        data = request.get_json()
        return TeacherSubjectUtils.create_teacher_subject(data)


class TeacherSubjectByTeacherId(Resource):
    def delete(self, teacher_id):
        return TeacherSubjectUtils.delete_teacher_subject_by_teacher_id(teacher_id)
