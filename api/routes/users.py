from flask import request, jsonify
from . import main
from models import db, User
from utils.hash_utils import hash_password, check_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# Login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'user_id': user.user_id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }), 200

# Register
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400
    hashed_password = hash_password(data['password'])
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        phone=data.get('phone'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'user_id': new_user.user_id,
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name
        }
    }), 201

# Refresh token
@main.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200

# Utility function to find user
def find_user(identifier, by_email=False):
    return User.query.filter_by(email=identifier).first() if by_email else User.query.get(identifier)

# Create user
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = hash_password(data['password'])
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        phone=data.get('phone'),
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Get all users
@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

# Update user
@main.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = find_user(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    for key in ['email', 'password', 'phone', 'first_name', 'last_name']:
        if key in data:
            setattr(user, key, hash_password(data[key]) if key == 'password' else data[key])
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Find user by email or ID
@main.route('/users/find', methods=['GET'])
def get_user():
    email = request.args.get('email')
    user_id = request.args.get('id', type=int)
    
    user = find_user(email, by_email=True) if email else find_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.serialize())