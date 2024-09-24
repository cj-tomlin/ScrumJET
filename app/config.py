import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b74cbe400be677ef6b4f21602d4899988a0eec844b06eab306cbba0cf2e07ea5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///scrumjet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
