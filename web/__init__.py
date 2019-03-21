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
from web.controller.attestation_controller import CreateAttestation
from web.controller.subject_controller import CreateSubject, CreateTeacherSubject, TeacherSubjectByTeacherId
from web.controller.analytics_controller import CountSubjectTeachers, GetTeachersAllSubjectsOfDepartment, \
    CreateFiveYearsPlan
from web.controller.extra_app_controller import CreateExtraApplication

api.add_resource(UserController, '/api/user', endpoint='user')  # TODO: delete endpoint
api.add_resource(UserLogin, '/api/login', endpoint='login')
api.add_resource(UserRegister, '/api/register', endpoint='register')

api.add_resource(CreateTeacher, '/api/teacher', endpoint='teacher')
api.add_resource(TeacherById, '/api/teacher/<teacher_id>', endpoint='teacher/<teacher_id>')

api.add_resource(GetAllTeachers, '/api/teachers', endpoint='teachers')
api.add_resource(GetFilteredTeachers, '/api/teachers/filtered', endpoint='teachers/filtered')

api.add_resource(CreateAttestation, '/api/attestation', endpoint='attestation')

api.add_resource(TeacherUserProfile, '/api/profile', endpoint='profile')

api.add_resource(CreateSubject, '/api/subject', endpoint='subject')
api.add_resource(CreateTeacherSubject, '/api/teachersubject', endpoint='teachersubject')

api.add_resource(TeacherSubjectByTeacherId, '/api/teachersubject/<teacher_id>', endpoint='teachersubject/<teacher_id>')

api.add_resource(CountSubjectTeachers, '/api/analytics/count_subject_teachers', endpoint='analytics/count_subject_teachers')
api.add_resource(GetTeachersAllSubjectsOfDepartment, '/api/analytics/all_subjects_dep',
                 endpoint='analytics/all_subjects_dep')

api.add_resource(CreateFiveYearsPlan, '/api/analytics/plan', endpoint='analytics/plan')

api.add_resource(CreateExtraApplication, '/api/application/extra', endpoint='application/extra')


@app.route("/")
def enter_data():
    return "Hello to attestation!!!!"


if __name__ == ' __main__':
    app.run(debug=True)
