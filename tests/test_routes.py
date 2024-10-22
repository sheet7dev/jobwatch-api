import pytest
from app import create_app
from flask_jwt_extended import create_access_token
from app.models import db, User
from config import TestingConfig


@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_config=TestingConfig)

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='module')
def auth_headers():
    user = User(email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {access_token}'}

def test_add_application(test_client, auth_headers):
    response = test_client.post('/api/applications', json={
        'company_name': 'Test Company',
        'job_position': 'Test Position',
        'job_link': 'http://example.com'
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['message'] == 'Application added'

def test_get_applications(test_client, auth_headers):
    response = test_client.get('/api/applications', headers=auth_headers)
    assert response.status_code == 200

def test_get_company_name(test_client, auth_headers):
    response = test_client.get('/api/applications?company_name=Test', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_job_position(test_client, auth_headers):
    response = test_client.get('/api/applications?job_position=Test', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_application(test_client, auth_headers):
    response = test_client.get('/api/applications/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_get_application_not_found(test_client, auth_headers):
    response = test_client.get('/api/applications/2', headers=auth_headers)
    assert response.status_code == 404
    assert response.json['message'] == 'Application not found'

def test_update_application(test_client, auth_headers):
    response = test_client.patch('/api/applications/1', json={
        'status': 'success'
    }, headers=auth_headers)
    assert response.status_code == 200

def test_update_aplication_not_found(test_client, auth_headers):
    response = test_client.patch('/api/applications/2', json={
        'status': 'success'
    }, headers=auth_headers)
    assert response.status_code == 404
    assert response.json['message'] == 'Application not found'

def test_update_application_invalid_status(test_client, auth_headers):
    response = test_client.patch('/api/applications/1', json={
        'status': 'invalid'
    }, headers=auth_headers)
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid status'

def test_update_application_unauthorized(test_client):
    response = test_client.patch('/api/applications/1')
    assert response.status_code == 415