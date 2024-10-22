from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Application


api_bp = Blueprint('api', __name__)

from .auth import auth_bp
api_bp.register_blueprint(auth_bp)


@api_bp.route('/applications', methods=['POST'])
@jwt_required()
def add_application():
    user_id = get_jwt_identity()
    data = request.get_json()
    company_name = data.get('company_name')
    job_position = data.get('job_position')
    submission_date = data.get('submission_date')
    job_link = data.get('job_link')

    new_application = Application(
        user_id = user_id,
        company_name = company_name,
        job_position = job_position,
        submission_date = submission_date,
        job_link = job_link)
    db.session.add(new_application)
    db.session.commit()

    return jsonify({"message": "Application added"}), 201


@api_bp.route('/applications/<int:app_id>', methods=['PATCH'])
@jwt_required(optional=True)
def update_application(app_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    status = data.get('status')

    application = Application.query.filter_by(id=app_id, user_id=user_id).first()
    if not application:
        return jsonify({"message": "Application not found"}), 404

    if status not in ['pending', 'failure', 'success']:
        return jsonify({"message": "Invalid status"}), 400

    application.status = status
    db.session.commit()
    return jsonify({"message": "Application updated"}), 200


@api_bp.route('/applications', methods=['GET'])
@jwt_required(optional=True)
def get_applications():
    user_id = get_jwt_identity()
    status_filter = request.args.get('status')
    search_query = request.args.get('search')

    query = Application.query.filter_by(user_id=user_id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    if search_query:
        search = f"%{search_query}%"
        query = query.filter_by(
            (Application.company_name.ilike(search)) |
            (Application.job_position.ilike(search))
        )

    applications = query.all()
    result = []
    for app in applications:
        result.append({
            'id': app.id,
            'company_name': app.company_name,
            'job_position': app.job_position,
            'submission_date': app.submission_date,
            'job_link': app.job_link,
            'status': app.status
        })

    return jsonify(result), 200

@api_bp.route('applications/<int:app_id>', methods=['GET'])
@jwt_required(optional=True)
def get_application(app_id):
    user_id = get_jwt_identity()
    application = Application.query.filter_by(id=app_id, user_id=user_id).first()
    if not application:
        return jsonify({"message": "Application not found"}), 404

    return jsonify({
        'id': application.id,
        'company_name': application.company_name,
        'job_position': application.job_position,
        'submission_date': application.submission_date,
        'job_link': application.job_link,
        'status': application.status
    }), 200

