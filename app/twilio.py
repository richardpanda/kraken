from flask import current_app
from twilio.rest import Client


def create_twilio_client():
    return Client(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
