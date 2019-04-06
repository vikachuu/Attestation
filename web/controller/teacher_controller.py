from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from web.service.authorization_utils import Register
from web.service.subject_utils import TeacherSubjectUtils
from web.service.teacher_utils import TeacherUtils


class CreateTeacher(Resource):
    @staticmethod
    def create_teacher_subjects(post_data):
        personnel_number = post_data['personnel_number']
        for subject in post_data.get('subjects', []):
            data = {
                "subject_id": subject['subject_id'],
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
        try:
            response = TeacherUtils.delete_teacher_by_id(teacher_id)
        except IntegrityError as e:
            return "Cannot delete teacher while his attestation present\nError: {}".format(e), 400
        return response

    def put(self, teacher_id):
        put_data = request.get_json()
        personnel_number = put_data.get("personnel_number")
        TeacherSubjectUtils.delete_teacher_subject_by_teacher_id(personnel_number)
        CreateTeacher.create_teacher_subjects(put_data)
        return TeacherUtils.update_teacher_by_id(teacher_id, put_data)

    def patch(self, teacher_id):
        patch_data = request.get_json()
        return TeacherUtils.update_teacher_next_attestation_year(teacher_id, patch_data['next_attestation_date'])


class GetAllTeachers(Resource):

    def get(self):
        return TeacherUtils.get_all_teachers()


class GetFilteredTeachers(Resource):

    def get(self):
        return TeacherUtils.get_filtered_teachers(request.args)
