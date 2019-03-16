from flask import request
from flask_restful import Resource

from web.service.user_utils import UserUtils


class UserController(Resource):
    def get(self):
        request_data = request.get_json()
        print(request.args.get('data'))
        print(request.args['data'])
        return "User get"

    def post(self):
        return "User post"


class TeacherUserProfile(Resource):
    def get(self):
        token = request.headers.get('token')
        return UserUtils.get_teacher_user_profile(token)
