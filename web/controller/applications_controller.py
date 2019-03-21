from flask import request
from flask_restful import Resource

from web.service.applications_utils import ExtraApplicationUtils, DefermentApplicationUtils


class ExtraApplication(Resource):
    def post(self):
        data = request.get_json()
        return ExtraApplicationUtils.create_extra_application(data)

    def get(self):
        filters = request.args
        return ExtraApplicationUtils.get_filtered_extra_applications(filters)


class ExtraApplicationById(Resource):
    def put(self, application_id):
        data = request.get_json()
        return ExtraApplicationUtils.update_extra_application(application_id, data)


class CountExtraApplications(Resource):
    def get(self):
        filters = request.args
        return ExtraApplicationUtils.count_filtered_extra_applications(filters)


class DefermentApplication(Resource):
    def post(self):
        data = request.get_json()
        return DefermentApplicationUtils.create_deferment_application(data)
