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
