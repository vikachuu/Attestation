from flask import request
from flask_restful import Resource


class UserController(Resource):
    def get(self):
        request_data = request.get_json()
        print(request.args.get('dat'))
        print(request.args['data'])
        return "User get"

    def post(self):
        return "User post"
