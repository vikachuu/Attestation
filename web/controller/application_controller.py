from flask import request
from flask_restful import Resource

from web.service.application_utils import ExtraApplicationUtils


class CreateExtraApplication(Resource):
    def post(self):
        data = request.get_json()
        return ExtraApplicationUtils.create_extra_application(data)


class ExtraApplicationById(Resource):
    def put(self, application_id):
        data = request.get_json()
        return ExtraApplicationUtils.update_extra_application(application_id, data)
