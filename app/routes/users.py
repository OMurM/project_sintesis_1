from flask import request, jsonify
from . import main
from models import db, User
from utils.hash_utils import hashed_password, check_password

@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hash_password = hash_password(data.get('password'))
    new_user = User(email=data['email'], password=hashed_password, phone=data.get('phone'), first_name=data['first_name'], last_name=data['last_name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'email': user.email, 'phone': user.phone, 'first_name': user.first_name, 'last_name': user.last_name} for user in users])

@main.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.email = data['email']
    user.password = hashed_password(data['password'])
    user.phone = data.get('phone')
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@main.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})