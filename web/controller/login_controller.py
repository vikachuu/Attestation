from flask import request
from flask_restful import Resource

from web.service.authorization_utils import Authorization, Register


class UserLogin(Resource):

    def post(self):
        """Login user"""
        # get the post data
        post_data = request.get_json()
        return Authorization.login_user(data=post_data)


class UserRegister(Resource):
    def post(self):
        post_data = request.get_json()
        return Register.register_user(data=post_data)
