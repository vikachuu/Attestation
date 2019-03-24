from flask import request
from flask_restful import Resource
from web import excel

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
        query_set = TeacherAnalyticsUtils.get_five_years_plan_document()
        column_names = ['прізвище', 'ім\'я', 'по-батькові',
                        'категорія', 'звання', 'дата попередньої атсетації', 'дата настпуної атестації']
        return excel.make_response_from_query_sets(query_set, column_names, "xlsx")


class GetTeachersCurrentYearAttestation(Resource):
    def get(self):
        return TeacherAnalyticsUtils.get_teachers_current_year_attestation()
