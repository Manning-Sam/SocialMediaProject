import os

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENVE = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATION=False
    SECRET_KEY=os.environ.get('SECRET_KEY')