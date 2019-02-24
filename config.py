DEBUG = True

SECRET_KEY = 'secretkey'

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'vikachu'
POSTGRES_DB = 'attestation'

SQLALCHEMY_DATABASE_URI = 'postgres://etdhfamqqwvrix:88ea5ab143acd04c0443e09f7ddebbcf6042d7aa7009d0373b4de8d04a01cd75@ec2-107-20-185-27.compute-1.amazonaws.com:5432/d1i7jk1h47bbs8'

# SQLALCHEMY_DATABASE_URI = 'postgres://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@localhost/' + POSTGRES_DB
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_HEADERS = 'Content-Type'
