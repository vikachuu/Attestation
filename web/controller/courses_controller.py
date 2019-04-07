from flask import request
from flask_restful import Resource

from web.service.courses_utils import CoursesUtils


class CreateCourses(Resource):
    def post(self):
        post_data = request.get_json()

        # create selective courses
        selective_courses = post_data.get('selective_courses')
        referral_number = post_data.get('referral_number')
        if len(selective_courses) < 5:
            return {"message": "number of selective courses should be 5."}, 400

        referral_response = CoursesUtils.create_referral_to_courses(post_data)
        for course in selective_courses:
            CoursesUtils.create_date_of_course(course, referral_number)

        return referral_response


class ReferralToCoursesById(Resource):
    def put(self, referral_id):
        put_data = request.get_json()
        selective_courses = put_data.get('selective_courses')
        if len(selective_courses) < 5:
            return {"message": "number of selective courses should be 5."}, 400

        referral_update_response = CoursesUtils.update_referral_to_courses_by_id(put_data, referral_id)
        for course in selective_courses:
            CoursesUtils.update_date_of_course(course, course.get('date_of_course_id'), referral_id)

        return referral_update_response

    def delete(self, referral_id):
        return CoursesUtils.delete_referral_to_courses_by_id(referral_id)


class AllTeachersWithCourses(Resource):
    def get(self):
        return CoursesUtils.get_all_teachers_with_courses()


class AllTeachersSubjectsWithCourses(Resource):
    def get(self):
        return CoursesUtils.get_all_teachers_of_subject_with_courses(request.args)
