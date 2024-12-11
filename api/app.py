from flask import Flask, send_from_directory
from config import Config
from models import db
from routes import main
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Set up Flask-JWT-Extended 
app.config['JWT_SECRET_KEY'] = 'supersecretpassword'
jwt = JWTManager(app)

app.register_blueprint(main)

@app.route('/images/<filename>')
def serve_image(filename):
    image_directory = '/home/2DAM/images' 
    return send_from_directory(image_directory, filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
