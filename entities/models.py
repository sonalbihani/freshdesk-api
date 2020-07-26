from sqlalchemy import Column, String, Integer,DateTime
from marshmallow import Schema, fields
from .entity import Entity, Base
from datetime import datetime,timedelta

class Tickets(Entity, Base):
    __tablename__ = 'tickets'
    subject = Column(String)
    description = Column(String)
    requester_id = Column(Integer)
    responder_id = Column(Integer)
    status = Column(Integer)
    source = Column(Integer)
    due_by = Column(DateTime)
    category = Column(Integer)
    def __init__(self, subject, description,category,requester_id,responder_id,status=2,source=2):
        Entity.__init__(self)
        self.subject = subject
        self.description = description
        self.due_by = datetime.now() +timedelta(days=30)
        self.category = category
        self.requester_id = requester_id
        self.responder_id = responder_id
        self.status = status
        self.source = source

class TicketSchema(Schema):
    id = fields.Number()
    subject = fields.Str()
    description = fields.Str()
    status = fields.Int()
    source = fields.Int()
    due_by = fields.DateTime()
    responder_id = fields.Int()
    requester_id = fields.Int()
    category = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class Contacts(Entity, Base):
    __tablename__ = 'contacts'
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    def __init__(self,name,email,phone=None,company_name=None):
        Entity.__init__(self)
        self.name = name
        self.email = email
        self.phone = phone
        self.company_name = company_name

class ContactSchema(Schema):
    id = fields.Number(),
    name = fields.Str(),
    email = fields.Str(),
    phone = fields.Str(),
    company_name = fields.Str(),
    created_at = fields.DateTime(),
    updated_at = fields.DateTime()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    fname = Column(String)
    lname = Column(String)
    def __init__(self, email, password,fname,lname=''):
        self.email = email
        self.password = password
        self.fname =fname
        self.lname =lname


class UserSchema(Schema):
    id = fields.Number(),
    fname = fields.Str(allow_none=True),
    lname = fields.Str(allow_none=True),
    email = fields.Str(allow_none=True),
    password = fields.Str()


