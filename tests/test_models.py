import pytest
from app.models import User, Application

@pytest.fixture(scope='module')
def new_user():
    user = User(email ='email1@example.com', password_hash ='examplepassword1')
    return user

@pytest.fixture(scope='module')
def new_application(new_user):
    application = Application(
        company_name='Company1',
        job_position='Position1',
        submission_date='2021-01-01',
        job_link='www.example.com',
        status='pending',
        user=new_user
        )
    return application


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and hashed_password
    """
    assert new_user.email == 'email1@example.com'
    assert new_user.password_hash == 'examplepassword1'


def test_new_application(new_application):
    """
    GIVEN an Application model
    WHEN a new Application is created
    THEN check the company_name, job_position, submission_date, job_link, and status
    """
    assert new_application.company_name == 'Company1'
    assert new_application.job_position == 'Position1'
    assert new_application.submission_date == '2021-01-01'
    assert new_application.job_link == 'www.example.com'
    assert new_application.status == 'pending'


def test_application_is_attached_to_user(new_application, new_user):
    """
    GIVEN a Application model
    WHEN a new Application is created
    THEN check the company_name, job_position, submission_date, job_link, status, and user
    """
    assert new_application.company_name == 'Company1'
    assert new_application.job_position == 'Position1'
    assert new_application.submission_date == '2021-01-01'
    assert new_application.job_link == 'www.example.com'
    assert new_application.status == 'pending'
    assert new_application.user == new_user


def test_user_has_one_application(new_application, new_user):
    """
    GIVEN a User model
    WHEN a new Application is created
    THEN check the number of applications attached to the user
    """
    assert len(new_user.applications) == 1
    assert new_user.applications[0] == new_application
