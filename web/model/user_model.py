import jwt
import datetime
from web import db, flask_bcrypt, app


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)

    personnel_number = db.Column(db.Integer, db.ForeignKey('teacher.personnel_number'), nullable=True)
    teacher = db.relationship("Teacher", back_populates="user")

    def __init__(self, login, password, access_level=0, personnel_number=None):
        self.login = login
        self.password = flask_bcrypt.generate_password_hash(password).decode()
        self.access_level = access_level
        self.personnel_number = personnel_number

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),  # TODO: edit expiration date
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
