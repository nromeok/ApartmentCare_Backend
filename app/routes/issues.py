from app.models import Issue, User
from flask import Blueprint, jsonify, request
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

issues_bp =Blueprint("issues",__name__)

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

@issues_bp.route("/issues", methods=["POST"])
@jwt_required()
def get_issues():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.role == "admin":
        issues = Issue.query.order_by(Issue.created_at.desc()).all()
    else:
        issues = Issue.query.filter_by(user_id=current_user.id).order_by(Issue.created_at.desc()).all()
    return jsonify({"issues": [issue.to_dict() for issue in issues]}), 200

@issues_bp.route("/issues", methods=["POST"])
@jwt_required()
def create_issue():
    current_user = get_current_user()

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.role ==  "admin":
        return jsonify({"error": "Admins cannot create issues"}), 403

    data = request.get_json() or {}
    description = data.get("description", "").strip()

    if not description:
        return jsonify({"error": "Description is required"}), 400

    issue = Issue(
        user_id=current_user.id,
        house_number=current_user.house_number,
        description=description,
        status = "Pending"
    )
    db.session.add(issue)
    db.session.commit()
    return jsonify({"message": "Issue created successfully", "issue": issue.to_dict()}), 201

@issues_bp.route("/<int:issue_id>", methods=["PATCH"])
@jwt_required()
def update_issue_status(issue_id):
    current_user = get_current_user()

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.role != "admin":
        return jsonify({"error": "Only admins can update issue status"}), 403

    issue = Issue.query.get(issue_id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    data = request.get_json() or {}
    new_status = data.get("status", "").strip()

    allowed_statuses = ["Pending", "In Progress", "Resolved"]
    if new_status not in allowed_statuses:
        return jsonify({"error": "Invalid status value"}), 400

    issue.status = new_status
    db.session.commit()
    return jsonify({"message": "Issue status updated successfully", "issue": issue.to_dict()}), 200