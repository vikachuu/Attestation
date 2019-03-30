from flask import request
from flask_restful import Resource
from datetime import datetime
from web.service.applications_utils import ExtraApplicationUtils, DefermentApplicationUtils
from web.service.teacher_utils import TeacherUtils


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
        if data.get('extra_application_status') == "CONFIRMED":
            TeacherUtils.update_teacher_next_attestation_year(data.get('personnel_number'), datetime.now().year + 1)
        return ExtraApplicationUtils.update_extra_application(application_id, data)


class CountExtraApplications(Resource):
    def get(self):
        filters = request.args
        return ExtraApplicationUtils.count_filtered_extra_applications(filters)


class DefermentApplication(Resource):
    def post(self):
        data = request.get_json()
        return DefermentApplicationUtils.create_deferment_application(data)

    def get(self):
        filters = request.args
        return DefermentApplicationUtils.get_filtered_deferment_applications(filters)


class DefermentApplicationById(Resource):
    def put(self, application_id):
        data = request.get_json()
        next_date = TeacherUtils.get_next_attestation_date_by_id(data.get('personnel_number'))
        if data.get('deferment_application_status') == "CONFIRMED":
            TeacherUtils.update_teacher_next_attestation_year(data.get('personnel_number'), int(next_date) +
                                                              data.get('deferment_application_years'))
        return DefermentApplicationUtils.update_deferment_application(application_id, data)


class CountDefermentApplications(Resource):
    def get(self):
        filters = request.args
        return DefermentApplicationUtils.count_filtered_deferment_applications(filters)
