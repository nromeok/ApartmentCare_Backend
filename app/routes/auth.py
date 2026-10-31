import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    house_number = data.get("house_number", "").strip()
    password = data.get("password", "")

    if not all([name, email, house_number, password]):
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    if User.query.filter_by(house_number=house_number).first():
        return jsonify({"error": "House number already exists"}), 409

    user = User(
        name=name,
        email=email,
        house_number=house_number,
        role="user"
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Account created successfully",
        "access_token": access_token,
        "user": user.to_dict()
    }), 201


@auth_bp.route("/register-admin", methods=["POST"])
def register_admin():
    data = request.get_json() or {}

    # Check the secret key
    admin_secret = data.get("admin_secret", "")
    expected_secret = os.getenv("ADMIN_SECRET")

    if not expected_secret or admin_secret != expected_secret:
        return jsonify({"error": "Invalid admin secret"}), 403

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    house_number = data.get("house_number", "").strip()
    password = data.get("password", "")

    if not all([name, email, house_number, password]):
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    if User.query.filter_by(house_number=house_number).first():
        return jsonify({"error": "House number already exists"}), 409

    user = User(
        name=name,
        email=email,
        house_number=house_number,
        role="admin"
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Admin account created successfully",
        "access_token": access_token,
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    house_number = data.get("house_number", "").strip()
    password = data.get("password", "")

    if not house_number or not password:
        return jsonify({"error": "House number and password are required"}), 400

    user = User.query.filter_by(house_number=house_number).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200