from flask import Blueprint, request, jsonify
import models
from utils import hash_password

bp = Blueprint('users', __name__)

@bp.route('/', methods=['GET'])
def home():
    return "User Management System"

@bp.route('/users', methods=['GET'])
def get_users():
    users = models.get_all_users()
    users_list = [dict(user) for user in users]
    return jsonify(users_list)

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = models.get_user_by_id(user_id)
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    email = data['email']
    password = data['password']

    existing_user = models.get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409

    password_hash = hash_password(password)

    user_id = models.create_user(name, email, password_hash)
    return jsonify({"message": "User created", "user_id": user_id}), 201

@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    user = models.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    models.update_user(user_id, name, email)
    return jsonify({"message": "User updated"}), 200

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = models.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    models.delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted"}), 200

@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    users = models.search_users_by_name(name)
    users_list = [dict(user) for user in users]
    return jsonify(users_list)
