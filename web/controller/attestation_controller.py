from flask import request
from flask_restful import Resource

from web.service.attestation_utils import AttestationUtils


class CreateAttestation(Resource):

    def post(self):
        post_data = request.get_json()
        token = request.headers.get('token')

        return AttestationUtils.create_attestation(post_data, token)
