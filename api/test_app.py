import json
import os
import pytest

from app import app as _app
from db import db_session, init_db, clear_db
from models import User
from unittest.mock import patch


@pytest.fixture(scope='module')
def app():
    return _app.test_client()


@pytest.fixture
def db():
    init_db()
    yield
    clear_db()


@pytest.fixture
def session():
    yield db_session
    db_session.remove()


@patch('app.twilio_client')
def test_register(twilio_client, app, db, session):
    assert session.query(User).count() == 0

    request_body = {
        'phone_number': '+12345678999',
        'start_time': '08:00',
        'end_time': '22:00',
    }
    response = app.post('/api/register', data=request_body)
    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['success'] is True
    assert session.query(User).count() == 1

    user = session.query(User).first()
    assert user.code is not None
    assert len(user.code) == 6

    twilio_client.api.account.messages.create.assert_called_with(
        to='+12345678999',
        from_=os.environ['KRAKEN__TWILIO__TEST_PHONE_NUMBER'],
        body=f'Your code is {user.code}')
