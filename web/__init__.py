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
from web.controller.subject_controller import CreateSubject, CreateTeacherSubject

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


@app.route("/")
def enter_data():
    return "Hello to attestation!!!!"


if __name__ == ' __main__':
    app.run(debug=True)
