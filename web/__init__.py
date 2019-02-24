from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
heroku = Heroku(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


from web.controller.login_controller import UserLogin, UserRegister
from web.controller.user_controller import UserController

api.add_resource(UserController, '/api/user', endpoint='user')
api.add_resource(UserLogin, '/api/login', endpoint='login')
api.add_resource(UserRegister, '/api/register', endpoint='register')


@app.route("/")
# @cross_origin()
def enter_data():
    return "Hello world!!!!"


# @app.route("/api/ping")
# def ping():
#     return jsonify({"status": 200, "msg": "This message is coming from Flask backend!"})


if __name__ == ' __main__':
    app.run(debug=True)
