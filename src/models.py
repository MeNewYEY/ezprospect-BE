from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    # firstname = db.Column(db.varchar(250), unique=False, nullable=False)
    # lastname = db.Column(db.varchar(250), unique=False, nullable=False)
    # phonenumber = db.Column(db.varchar(50), unique=False, nullable=False)
    # reset_password_token = db.Column(db.String(80), unique=False, nullable=False)
    # reset_password_expiration = db.Column(db.String(80), unique=False, nullable=False)
    # created_at = db.Column(db.String(80), unique=False, nullable=False)
    # modified_at = db.Column(db.String(80), unique=False, nullable=False)    
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
    # organization = relationship(Organization)

    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.is_active=True


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

# class Prospects(db.Model):
#     __tablename__ = 'prospects'
#     prospect_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Varchar(250), unique=True, nullable=False)
#     industry = db.Column(db.Varchar(250), unique=False, nullable=False)
#     address1 = db.Column(db.varchar(250), unique=False, nullable=False)
#     address2 = db.Column(db.varchar(250), unique=False, nullable=False)
#     city = db.Column(db.varchar(250), unique=False, nullable=False)
#     state = db.Column(db.varchar(250), unique=False, nullable=False)
#     background = db.Column(db.String(80), unique=False, nullable=False)
#     created_at = db.Column(db.String(80), unique=False, nullable=False)
#     modified_at = db.Column(db.String(80), unique=False, nullable=False)    
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

# class Contacts(db.Model):
#     __tablename__ = 'contacts'
#     contact_id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.Varchar(250), unique=True, nullable=False)
#     lastname = db.Column(db.Varchar(250), unique=False, nullable=False)
#     position = db.Column(db.String(250), unique=False, nullable=False)
#     title = db.Column(db.String(250), unique=False, nullable=False)
#     email_address = db.Column(db.String(250), unique=False, nullable=False)
#     phone = db.Column(db.String(250), unique=False, nullable=False)
#     created_at = db.Column(db.String(80), unique=False, nullable=False)
#     modified_at = db.Column(db.String(80), unique=False, nullable=False)    
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

# class Clients(db.Model):
#     __tablename__ = 'clients'
#     client_id = db.Column(db.Integer, primary_key=True)      
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)
#     prospect_id = db.Column(Integer, ForeignKey('prospect.prospect_id'))
#     prospect = relationship(Prospects)
#     user_id = db.Column(Integer, ForeignKey('user.user_id'))
#     user = relationship(User)
#     organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
#     organization = relationship(Organization)
#     product_id = db.Column(Integer, ForeignKey('product.product_id'))
#     product = relationship(Product)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }


# class Product(db.Model):
#     __tablename__ = 'product'
#     product_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), unique=False, nullable=False)
#     description = db.Column(db.String(250), unique=False, nullable=False)
#     status = db.Column(db.Boolean(), unique=False, nullable=False)
#     organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
#     organization = relationship(Organization)

#     def __repr__(self):
#         return '<Todo %r>' % self.label

#     def serialize(self):
#         return {
#             "done": self.done,
#             "label": self.label,
#             # do not serialize the password, its a security breach
#         }


# class Organization(db.Model):
#     __tablename__ = 'organization'
#     organization_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=True, nullable=False)
#     address1 = db.Column(db.String(80), unique=False, nullable=False)
#     address2 = db.Column(db.String(80), unique=False, nullable=False)
#     city = db.Column(db.String(80), unique=False, nullable=False)
#     state = db.Column(db.String(80), unique=False, nullable=False)
#     zip = db.Column(db.Integer, unique=False, nullable=False)
#     phone = db.Column(db.Varchar(50), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }
