from flask import request
from flask_restful import Resource


class UserController(Resource):
    def get(self):
        return "User get"

    def post(self):
        return "User post"
