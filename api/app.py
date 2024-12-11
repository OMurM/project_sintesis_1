from flask import Flask
from config import Config
from models import db
from routes import main
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Set up Flask-JWT-Extended 
app.config['JWT_SECRET_KEY'] = 'supersecretpassword'
jwt = JWTManager(app)

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)