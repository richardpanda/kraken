from app import db

from .utils import generate_code


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(12), unique=True)
    start_hour = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    code = db.Column(db.String(6), default=generate_code())
    is_pending = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User id={self.id} phone_number={self.phone_number} start_hour={self.start_hour} end_hour={self.end_hour} code={self.code}>'
