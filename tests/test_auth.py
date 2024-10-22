import pytest
from app import create_app
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
def new_user():
    user = User(email='tester@example.com')
    user.set_password('password123')
    return user


def test_register(test_client):
    response = test_client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "User created"}


def test_register_existing_user(test_client, new_user):
    db.session.add(new_user)
    db.session.commit()

    response = test_client.post('/api/register', json={
        'email': 'tester@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.get_json() == {"message": "User already exists"}

def test_login(test_client, new_user):
    db.session.add(new_user)
    db.session.commit()

    response = test_client.post('/api/login', json={
        'email': 'tester@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_credentials(test_client):
    response = test_client.post('/api/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid credentials"}