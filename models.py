from application import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):

    id = db.Column(db.String(), nullable=False, primary_key=True)  # Facebook id
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    property_value = db.Column(db.String())
    mortgage_balance = db.Column(db.String())
    credit_score = db.Column(db.String())
    dob = db.Column(db.String())
    is_recent_bankruptcy = db.Column(db.String())
    is_recent_foreclosure = db.Column(db.String())
    street_address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zipcode = db.Column(db.String())
    messages = relationship('Message', back_populates="user")
    total_error_count = db.Column(db.Integer)
    current_scope = db.Column(db.String())
    current_scope_eror_count = db.Column(db.Integer)
    current_prompt = db.Column(db.String())
    current_prompt_eror_count = db.Column(db.Integer)
    sent_to_velocify = db.Column(db.Boolean(), default=False)

    def __init__(self, id):
        self.id = id


    def __repr__(self):
        return '<id {}>'.format(self.id)


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), ForeignKey('user.id'))
    user = relationship("User", back_populates="messages")
    sender = db.Column(db.String())  # fb_id of recipient
    recipient = db.Column(db.String())  # fb_id of recipient
    text = db.Column(db.String())
    photo = db.Column(db.String())  # URL


    def __init__(self, id):
        self.id = id


    def __repr__(self):
        return '<id {}>'.format(self.id)
