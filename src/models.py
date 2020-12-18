from flask_sqlalchemy import SQLAlchemy
from datetime import timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    # users_Prospects = db.relationship("Users_Prospects")

    # reset_password_token = db.Column(db.String(80), unique=False, nullable=False)
    # reset_password_expiration = db.Column(db.String(80), unique=False, nullable=False)
    # created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    # modified_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)    
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
    # organization = relationship(Organization)
# 
    def __init__(self,email,password,first_name,last_name,phone_number):
        self.email=email
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.is_active=True


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
            # "users_Prospects": list(map(lambda x: x.serialize(), self.users_Prospects))
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
    # users_prospects = db.relationship('Users_Prospects', backref='prospect', lazy=True)
    # background = db.Column(db.String(80), unique=False, nullable=False)
    # created_at = db.Column(db.String(80), unique=False, nullable=False)
    # modified_at = db.Column(db.String(80), unique=False, nullable=False)    
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
            # "users_Prospects": list(map(lambda x: x.serialize(), self.users_Prospects))
            # do not serialize the password, its a security breach
        }

# class Users_Prospects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey(user.id),
#         nullable=False)
#     prospect_id = db.Column(db.Integer, db.ForeignKey(prospect.id),
#         nullable=False)

#     def __repr__(self):
#         return f'<Users_Prospects {self.id}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id":self.user_id,
#             "prospect_id": self.prospect_id
#         }

# class Prospects_Contacts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     prospect_id = db.Column(db.Integer, db.ForeignKey(Prospects.id))
#     contact_id = db.Column(db.Integer, db.ForeignKey(Business.id))   



class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(250), unique=True, nullable=False)
    lastname = db.Column(db.String(250), unique=False, nullable=False)
    position = db.Column(db.String(250), unique=False, nullable=False)
    title = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    # created_at = db.Column(db.String(80), unique=False, nullable=False)
    # modified_at = db.Column(db.String(80), unique=False, nullable=False)    
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

    def __init__(self,firstname,lastname,position,title,email,zipCode,phone_number):
        self.firstname=firstname
        self.lastname=lastname
        self.position=position
        self.title=title
        self.email=email
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.is_active=True 

    def __repr__(self):
        return '<Contacts %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "position": self.position,
            "title": self.title,
            "email": self.email,
            "zipCode": self.zipCode,
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
    # organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
    # organization = relationship(Organization)

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
            # do not serialize the password, its a security breach
        }
