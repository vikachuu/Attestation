from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
heroku = Heroku(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from web.service.utils import CustomJSONEncoder  # uses User model -> local import
app.json_encoder = CustomJSONEncoder

from web.controller.login_controller import UserLogin, UserRegister
from web.controller.user_controller import UserController, TeacherUserProfile
from web.controller.teacher_controller import CreateTeacher, TeacherById, GetAllTeachers, GetFilteredTeachers
from web.controller.attestation_controller import Attestation, AttestationById
from web.controller.subject_controller import CreateSubject, CreateTeacherSubject, TeacherSubjectByTeacherId
from web.controller.analytics_controller import CountSubjectTeachers, GetTeachersAllSubjectsOfDepartment, \
    CreateFiveYearsPlan, GetTeachersCurrentYearAttestation, CreateFiveYearsPlanDocument
from web.controller.applications_controller import ExtraApplication, ExtraApplicationById, CountExtraApplications, \
    DefermentApplication, DefermentApplicationById, CountDefermentApplications
from web.controller.courses_controller import CreateCourses, ReferralToCoursesById, CreateDateOfCourse

# User
api.add_resource(UserController, '/api/user', endpoint='user')  # TODO: delete endpoint
api.add_resource(UserLogin, '/api/login', endpoint='login')
api.add_resource(UserRegister, '/api/register', endpoint='register')

# Teacher
api.add_resource(CreateTeacher, '/api/teacher', endpoint='teacher')
api.add_resource(TeacherById, '/api/teacher/<teacher_id>', endpoint='teacher/<teacher_id>')

api.add_resource(GetAllTeachers, '/api/teachers', endpoint='teachers')
api.add_resource(GetFilteredTeachers, '/api/teachers/filtered', endpoint='teachers/filtered')

# Attestation
api.add_resource(Attestation, '/api/attestation', endpoint='attestation')
api.add_resource(AttestationById, '/api/attestation/<attestation_number>', endpoint='attestation/<attestation_number>')

# Profile
api.add_resource(TeacherUserProfile, '/api/profile', endpoint='profile')

# Subjects
api.add_resource(CreateSubject, '/api/subject', endpoint='subject')
api.add_resource(CreateTeacherSubject, '/api/teachersubject', endpoint='teachersubject')

api.add_resource(TeacherSubjectByTeacherId, '/api/teachersubject/<teacher_id>', endpoint='teachersubject/<teacher_id>')

# Analytics
api.add_resource(CountSubjectTeachers, '/api/analytics/count_subject_teachers', endpoint='analytics/count_subject_teachers')
api.add_resource(GetTeachersCurrentYearAttestation, '/api/analytics/current_year_attestation', endpoint='analytics/current_year_attestation')
api.add_resource(GetTeachersAllSubjectsOfDepartment, '/api/analytics/all_subjects_dep', endpoint='analytics/all_subjects_dep')

# Attestation plan
api.add_resource(CreateFiveYearsPlan, '/api/analytics/plan', endpoint='analytics/plan')
api.add_resource(CreateFiveYearsPlanDocument, '/api/analytics/plan/download', endpoint='analytics/plan/download')

# Applications
api.add_resource(ExtraApplication, '/api/application/extra', endpoint='application/extra')
api.add_resource(CountExtraApplications, '/api/application/extra/count', endpoint='application/extra/count')
api.add_resource(ExtraApplicationById, '/api/application/extra/<application_id>', endpoint='application/extra/<application_id>')

api.add_resource(DefermentApplication, '/api/application/deferment', endpoint='application/deferment')
api.add_resource(CountDefermentApplications, '/api/application/deferment/count', endpoint='application/deferment/count')
api.add_resource(DefermentApplicationById, '/api/application/deferment/<application_id>', endpoint='application/deferment/<application_id>')

# Courses
api.add_resource(CreateCourses, '/api/courses', endpoint='courses')
api.add_resource(ReferralToCoursesById, '/api/courses/<referral_id>', endpoint='courses/<referral_id>')
api.add_resource(CreateDateOfCourse, '/api/selective_course', endpoint='selective_course')


@app.route("/")
def enter_data():
    return "Hello to attestation!!!!"


if __name__ == ' __main__':
    app.run(debug=True, host='0.0.0.0')
