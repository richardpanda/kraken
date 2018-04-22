import json
import unittest

from app import create_app, db
from app.models import User
from config import TestingConfig
from unittest.mock import patch


class APITests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.api.create_twilio_client')
    def test_register(self, twilio_client):
        request_body = {
            'phone_number': '+12345678999',
            'start_hour': 8,
            'end_hour': 22,
        }
        response = self.client.post('/api/register', data=request_body)

        self.assertEqual(response.status_code, 200)

        user = db.session.query(User).first()
        self.assertIsNotNone(user.code)
        self.assertEqual(len(user.code), 6)
        self.assertTrue(user.is_pending)

        twilio_client().api.account.messages.create.assert_called_with(
            to='+12345678999',
            from_=TestingConfig.TWILIO_PHONE_NUMBER,
            body=f'Your code is {user.code}')

    def test_register_with_existing_phone_number(self):
        user = User(phone_number='+12345678999',
                    start_hour=8,
                    end_hour=22)
        db.session.add(user)
        db.session.commit()

        request_body = {
            'phone_number': user.phone_number,
            'start_hour': user.start_hour,
            'end_hour': user.end_hour,
        }
        response = self.client.post('/api/register', data=request_body)
        response_body = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_body['message'],
                         'Phone number has been registered already.')


if __name__ == '__main__':
    unittest.main()
