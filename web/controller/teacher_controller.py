from flask import request
from flask_restful import Resource

from web.service.teacher_utils import TeacherUtils


class AddTeacher(Resource):

    def post(self):
        post_data = request.get_json()
        # token = request.headers.get('token')
        return TeacherUtils.create_teacher(post_data)
