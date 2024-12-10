import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://oscar:My5q1%21p%40ss2024%23@192.168.1.41/sintesis_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)