from flask import request
from flask_restful import Resource
from datetime import datetime
from web.service.attestation_utils import AttestationUtils
from web.service.teacher_utils import TeacherUtils


class Attestation(Resource):

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')

        attestation_response = AttestationUtils.create_attestation(post_data, token)

        if attestation_response[1] == 200:
            personnel_number = post_data.get('personnel_number')
            new_category = post_data.get('category_conclusion')
            new_rank = post_data.get('rank_conclusion')
            new_prev_date = datetime.strptime(post_data.get('attestation_date'), '%Y-%m-%d').year
            new_next_date = new_prev_date + 5

            TeacherUtils.update_teacher_after_attestation(personnel_number, new_category, new_rank, new_prev_date,
                                                          new_next_date)
        return attestation_response

    def get(self):
        filters = request.args
        return AttestationUtils.get_all_attestations_with_teachers(filters.get('year'))


class AttestationById(Resource):

    def delete(self, attestation_number):
        return AttestationUtils.delete_attestation_by_id(attestation_number)
