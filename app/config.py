import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://oscar:SecurePass123!@192.168.1.41/sintesis_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)