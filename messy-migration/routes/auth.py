from flask import Blueprint, request, jsonify
import models
from utils import verify_password

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']

    user = models.get_user_by_email(email)
    if user and verify_password(user['password'], password):
        return jsonify({"status": "success", "user_id": user['id']}), 200

    return jsonify({"status": "failed", "message": "Invalid credentials"}), 401
