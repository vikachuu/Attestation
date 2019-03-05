from flask import request
from flask_restful import Resource

from web.service.teacher_utils import TeacherUtils


class AddTeacher(Resource):

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')
        return TeacherUtils.create_teacher(post_data, token)


class GetTeacherById(Resource):

    def get(self, teacher_id):
        return TeacherUtils.get_teacher_by_id(teacher_id)


class GetAllTeachers(Resource):

    def get(self):
        return TeacherUtils.get_all_teachers()
