"""Керування реєстрацією та входом за допомогою JWT."""
"""Модуль розпізнавання користувачів."""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User, Cart

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Реєстрація та автоматичне створення кошика."""
    data = request.json
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    db.session.add(Cart(user_id=new_user.id))
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Вхід та видача JWT токена."""
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token), 200
    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Отримання даних профілю поточного користувача."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(id=user.id, username=user.username)