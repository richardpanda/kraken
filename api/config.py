import os


class Config():
    DATABASE_URI = 'postgresql://postgres@localhost:5432/kraken'
    TWILIO_ACCOUNT_SID = os.getenv('KRAKEN__TWILIO__ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('KRAKEN__TWILIO__AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('KRAKEN__TWILIO__PHONE_NUMBER', '')


class TestConfig():
    DATABASE_URI = 'postgresql://postgres@localhost:5432/kraken_test'
    TWILIO_ACCOUNT_SID = os.getenv('KRAKEN__TWILIO__TEST_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('KRAKEN__TWILIO__TEST_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('KRAKEN__TWILIO__TEST_PHONE_NUMBER', '')
