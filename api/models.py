from db import Base
from sqlalchemy import Column, Integer, String, Time


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(12), unique=True)
    start_time = Column(Time)
    end_time = Column(Time)
    code = Column(String(6))

    def __repr__(self):
        return f'<User id={self.id} phone_number={self.phone_number} start_time={self.start_time} end_time={self.end_time} code={self.code}>'
