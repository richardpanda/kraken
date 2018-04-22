from app import db
from flask import Blueprint, current_app, jsonify, make_response, request
from sqlalchemy import exists
from twilio.rest import Client

from .models import User
from .twilio import create_twilio_client

api = Blueprint('api', __name__)


@api.route('/register', methods=['POST'])
def register():
    twilio_client = create_twilio_client()

    phone_number = request.form['phone_number']
    start_hour = request.form['start_hour']
    end_hour = request.form['end_hour']

    user_exists = db.session.query(exists().where(
        User.phone_number == phone_number)).scalar()

    if user_exists:
        message = 'Phone number has been registered already.'
        return make_response(jsonify({'message': message}), 400)

    user = User(phone_number=phone_number,
                start_hour=start_hour,
                end_hour=end_hour)
    db.session.add(user)
    db.session.commit()

    twilio_client.api.account.messages.create(
        to=f'{user.phone_number}',
        from_=current_app.config['TWILIO_PHONE_NUMBER'],
        body=f'Your code is {user.code}')

    return make_response(jsonify({}), 200)
