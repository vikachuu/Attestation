from flask import request
from flask_restful import Resource
from datetime import datetime
from web.service.attestation_utils import AttestationUtils
from web.service.teacher_utils import TeacherUtils


class CreateAttestation(Resource):

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')

        personnel_number = post_data.get('personnel_number')
        new_category = post_data.get('category_conclusion')
        new_rank = post_data.get('rank_conclusion')
        new_prev_date = datetime.strptime(post_data.get('attestation_date'), '%Y-%m-%d').year
        new_next_date = new_prev_date + 5

        TeacherUtils.update_teacher_after_attestation(personnel_number, new_category, new_rank, new_prev_date,
                                                      new_next_date)

        return AttestationUtils.create_attestation(post_data, token)
