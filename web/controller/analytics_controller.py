from flask import request
from flask_restful import Resource
from web.service.plan_utils import FiveYearsPlanUtils
from web.service.teacher_analytics_utils import TeacherAnalyticsUtils


class CountSubjectTeachers(Resource):
    def get(self):
        return TeacherAnalyticsUtils.count_subjects_teachers()


class GetTeachersAllSubjectsOfDepartment(Resource):
    def get(self):
        return TeacherAnalyticsUtils.get_teachers_all_subjects_of_department(request.args)


class CreateFiveYearsPlan(Resource):
    def get(self):
        return TeacherAnalyticsUtils.get_five_years_plan()


class CreateFiveYearsPlanDocument(Resource):
    def get(self):
        return FiveYearsPlanUtils.get_five_years_plan_document()


class GetTeachersCurrentYearAttestation(Resource):
    def get(self):
        return TeacherAnalyticsUtils.get_teachers_current_year_attestation()


class CountTeacherExtraApplications(Resource):
    def get(self):
        return TeacherAnalyticsUtils.count_teachers_extra_applications()
