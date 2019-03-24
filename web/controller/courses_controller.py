from flask import request
from flask_restful import Resource

from web.service.courses_utils import CoursesUtils


class CreateCourses(Resource):
    def post(self):
        post_data = request.get_json()
        referral_response = CoursesUtils.create_referral_to_courses(post_data)

        # create selective courses
        selective_courses = post_data.get('selective_courses')
        if len(selective_courses) < 5:
            return {"message": "number of selective courses should be 5."}, 400
        for course in selective_courses:
            CoursesUtils.create_date_of_course(course)

        return referral_response


class ReferralToCoursesById(Resource):
    def put(self, referral_id):
        put_data = request.get_json()
        return CoursesUtils.update_referral_to_courses_by_id(put_data, referral_id)

    def delete(self, referral_id):
        return CoursesUtils.delete_referral_to_courses_by_id(referral_id)


class CreateDateOfCourse(Resource):
    def post(self):
        post_data = request.get_json()
        return CoursesUtils.create_date_of_course(post_data)
