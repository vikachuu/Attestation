from flask import request
from flask_restful import Resource

from web.service.authorization_utils import Register
from web.service.subject_utils import TeacherSubjectUtils
from web.service.teacher_utils import TeacherUtils


class CreateTeacher(Resource):
    def create_teacher_subjects(self, post_data):
        personnel_number = post_data['personnel_number']
        for subject_id in post_data.get('subjects', []):
            data = {
                "subject_id": subject_id,
                "personnel_number": personnel_number
            }
            TeacherSubjectUtils.create_teacher_subject(data)

    def create_user_for_teacher(self, post_data):
        password = "".join(post_data['birth_date'].split('-'))
        personnel_number = post_data['personnel_number']
        data = {
            'login': str(personnel_number),
            'password': password,
            'access_level': 0,
            'personnel_number': personnel_number
        }
        create_user_response = Register.register_user(data)
        return create_user_response

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')

        create_teacher_response = TeacherUtils.create_teacher(post_data, token)

        if create_teacher_response[1] == 200:
            self.create_teacher_subjects(post_data)  # TODO: what to do if fails?
            return self.create_user_for_teacher(post_data)
        else:
            return create_teacher_response


class TeacherById(Resource):

    def get(self, teacher_id):
        return TeacherUtils.get_teacher_by_id(teacher_id)

    def delete(self, teacher_id):
        return TeacherUtils.delete_teacher_by_id(teacher_id)

    def put(self, teacher_id):
        put_data = request.get_json()
        return TeacherUtils.update_teacher_by_id(teacher_id, put_data)


class GetAllTeachers(Resource):

    def get(self):
        return TeacherUtils.get_all_teachers()


class GetFilteredTeachers(Resource):

    def get(self):
        return TeacherUtils.get_filtered_teachers(request.args)
