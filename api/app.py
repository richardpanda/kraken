import env
import os
import random

from config import Config, TestConfig
from db import db_session
from flask import Flask, jsonify, request
from models import User
from string import ascii_uppercase, digits
from twilio.rest import Client

app = Flask(__name__)
config = TestConfig if env.is_testing else Config
twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def generate_code():
    return ''.join(random.choices(ascii_uppercase + digits, k=6))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/register', methods=['POST'])
def register():
    phone_number = request.form['phone_number']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    user = User(phone_number=phone_number,
                start_time=start_time,
                end_time=end_time,
                code=generate_code())
    db_session.add(user)
    db_session.commit()

    twilio_client.api.account.messages.create(
        to=f'{user.phone_number}',
        from_=config.TWILIO_PHONE_NUMBER,
        body=f'Your code is {user.code}')

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
