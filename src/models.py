from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime

db = SQLAlchemy()

user_prospects = db.Table('user_prospects',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("prospect_id", db.Integer, db.ForeignKey("prospects.id"), primary_key=True)
)

prospects_contacts = db.Table('prospects_contacts',
    db.Column("contact_id", db.Integer, db.ForeignKey("contacts.id"), primary_key=True),
    db.Column("prospect_id", db.Integer, db.ForeignKey("prospects.id"), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    userprospects = db.relationship('Prospects', secondary=user_prospects, backref=db.backref('prospectsuser', lazy='dynamic'))   
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __init__(self,email,password,first_name,last_name,phone_number):
        self.email=email
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "organization_id": self.organization_id
            # do not serialize the password, its a security breach
        }

class Prospects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    industry = db.Column(db.String(250), unique=False, nullable=False)
    address1 = db.Column(db.String(250), unique=False, nullable=False)
    city = db.Column(db.String(250), unique=False, nullable=False)
    state = db.Column(db.String(250), unique=False, nullable=False)
    zipCode = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    account = db.Column(db.String(250), unique=False, nullable=False)
    # background = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self,name,industry,address1,city,state,zipCode,phone_number,account):
        self.name=name
        self.industry=industry
        self.address1=address1
        self.city=city
        self.state=state
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.account=account
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<Prospects %r>' % self.account

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "address1": self.address1,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone_number": self.phone_number,
            "account": self.account
            # do not serialize the password, its a security breach
        }

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=True, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    position = db.Column(db.String(250), unique=False, nullable=False)
    title = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    prospectscontacts = db.relationship('Prospects', secondary=prospects_contacts, backref=db.backref('prospectscontacts', lazy='dynamic'))
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False) 
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

    def __init__(self,first_name,last_name,position,title,email,phone_number):
        self.first_name=first_name
        self.last_name=last_name
        self.position=position
        self.title=title
        self.email=email
        self.phone_number=phone_number
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<Contacts %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "position": self.position,
            "title": self.title,
            "email": self.email,
            "phone_number": self.phone_number
        }

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)      
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # prospect_id = db.Column(Integer, ForeignKey('prospect.prospect_id'))
    # prospect = relationship(Prospects)
    # user_id = db.Column(Integer, ForeignKey('user.user_id'))
    # user = relationship(User)
    # organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
    # organization = relationship(Organization)
    # product_id = db.Column(Integer, ForeignKey('product.product_id'))
    # product = relationship(Product)

    def __init__(self):
        # self.firstname=firstname
        # self.lastname=lastname
        # self.position=position
        # self.title=title
        # self.email=email
        # self.zipCode=zipCode
        # self.phone_number=phone_number
        self.is_active=True 

    def __repr__(self):
        return '<Clients %r>' % self.id

    def serialize(self):
        return {
            "id": self.id
            # do not serialize the password, its a security breach
        }


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    status = db.Column(db.Boolean(), unique=False, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __init__(self,name,description):
        self.name=name
        self.description=description
        self.is_active=True 

    def __repr__(self):
        return '<Products %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            # do not serialize the password, its a security breach
        }


class Organizations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address1 = db.Column(db.String(80), unique=False, nullable=False)
    address2 = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    zipCode = db.Column(db.Integer, unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    users = db.relationship('User', backref="organizations")
    products = db.relationship('Products', backref="organizations")
    

    def __init__(self,name,address1,address2,city,state,zipCode,phone_number):
        self.name=name
        self.address1=address1
        self.address2=address2
        self.city=city
        self.state=state
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.is_active=True 

    def __repr__(self):
        return '<Organizations %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone_number": self.phone_number,
            "users": list(map(lambda x: x.serialize(), self.users))
            # do not serialize the password, its a security breach
        }
