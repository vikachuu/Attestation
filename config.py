DEBUG = True

SECRET_KEY = 'secretkey'

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'vikachu'
POSTGRES_DB = 'attestation'

SQLALCHEMY_DATABASE_URI = 'postgres://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@localhost/' + POSTGRES_DB
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_HEADERS = 'Content-Type'
