from app.models import User, Announcement
from flask import Blueprint, jsonify, request
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

announcements_bp = Blueprint("announcements", __name__)

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

@announcements_bp.route("/announcements", methods=["GET"])
@jwt_required()
def get_announcements():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify({"announcements": [announcement.to_dict() for announcement in announcements]}), 200


@announcements_bp.route("/announcements", methods=["POST"])
@jwt_required() 
def creete_announcement():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.role != "admin":
        return jsonify({"error": "Only admins can create announcements"}), 403

    data = request.get_json() or {}
    message = data.get("content", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    announcement = Announcement(
        message=message,
        created_by=current_user.id
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify({"message": "Announcement created successfully", "announcement": announcement.to_dict()}), 201