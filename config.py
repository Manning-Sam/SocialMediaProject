import os

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENVE = os.environ.get('FLASK_ENV')