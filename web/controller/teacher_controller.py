from flask import request
from flask_restful import Resource

from web.service.authorization_utils import Register
from web.service.teacher_utils import TeacherUtils


class AddTeacher(Resource):

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')

        create_teacher_response = TeacherUtils.create_teacher(post_data, token)
        if create_teacher_response[1] == 200:
            password = "".join(post_data['birth_date'].split('/'))
            data = {
                'login': str(post_data['personnel_number']),
                'password': password,
                'access_level': 0,
                'personnel_number': post_data['personnel_number']
            }
            create_user_response = Register.register_user(data)
            return create_user_response
        else:
            return create_teacher_response


class GetTeacherById(Resource):

    def get(self, teacher_id):
        return TeacherUtils.get_teacher_by_id(teacher_id)


class GetAllTeachers(Resource):

    def get(self):
        return TeacherUtils.get_all_teachers()
