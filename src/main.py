"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
# from datetime import date, time, datetime
from models import db, User, Prospects, Contacts, Organizations
from flask_jwt_simple import (JWTManager, jwt_required, create_jwt, get_jwt_identity)
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = "jd"
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg" : "Missing JSON info request"}),400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg" : "Missing email parameter"}),400

    if not password:
        return jsonify({"msg" : "Missing password parameter"}),400

    specific_user = User.query.filter_by(
        email=email
    ).one_or_none()

    if isinstance(specific_user,User):
        if sha256_crypt.verify(password, specific_user.password):
            response={
                "jwt" : create_jwt(identity=specific_user.id),
                "user_id": specific_user.id
            }
            return jsonify(response),200 
        else:
            return jsonify({"msg" : "Wrong Password"}),400

    else:
        return jsonify({"msg" : "User not found"}),400


@app.route('/signup', methods=['POST'])
def handle_signup():
    
    input_data = request.json

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    first_name = params.get('first_name', None)
    last_name = params.get('last_name', None)
    phone_number = params.get('phone_number', None)
    organization_id = params.get('organization_id', None)

    if not email:
        return jsonify({"msg" : "Missing email"}),400

    if not password:
        return jsonify({"msg" : "Missing password"}),400
    
    if not first_name:
        return jsonify({"msg" : "Missing first name"}),400
    
    if not last_name:
        return jsonify({"msg" : "Missing last name"}),400
    
    if not phone_number:
        return jsonify({"msg" : "Missing phone number"}),400

    

    # if 'email' in input_data and 'password' in input_data and 'first_name' in input_data and 'last_name' in input_data and 'phone_number' in input_data and 'organization_id' in input_data:

    specific_user = User.query.filter_by(
        email=input_data['email']
    ).one_or_none()

    organization = Organizations.query.get(input_data['organization_id'])


    if isinstance(specific_user,User):
        return jsonify({"msg" : "Email already in use"}),400
    else:
        new_user= User(
            email = input_data['email'],
            password = sha256_crypt.encrypt(str(input_data['password'])),
            first_name = input_data['first_name'],
            last_name = input_data['last_name'],
            phone_number = input_data['phone_number']
        )
        organization.users.append(new_user)
        db.session.add(new_user)
        try:
            db.session.commit()
            response={
                "jwt" : create_jwt(identity=new_user.id),
                "user_id": new_user.id
            }
            return jsonify(response),200

        except Exception as error:
            db.session.rollback()
            return jsonify({"msg" : error}),500

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    specific_user_id = get_jwt_identity()
    specific_user = User.query.filter_by(
        id = specific_user_id
        ).one_or_none()

    if specific_user is None:
        return jsonify({"msg" : "user not found"}),404

    else:
        return jsonify(specific_user.serialize()),200

@app.route('/addProspect', methods=['POST'])
def add_prospect():
    input_data = request.json 
    user_id = input_data['user_id']

    new_prospect= Prospects(
        name = input_data['name'],
        industry = input_data['industry'],
        address1 = input_data['address1'],
        city = input_data['city'],
        state = input_data['state'],
        zipCode = input_data['zipCode'],
        phone_number = input_data['phone_number'],
        account = input_data['account']
    )

    user = User.query.filter_by(
        id=user_id
    ).one_or_none()    

    specific_prospect = Prospects.query.filter_by(
        account=input_data['account']
    ).one_or_none()

    if isinstance(specific_prospect,Prospects):
        prospect_id = specific_prospect.id
        prospects_query = User.query.filter(User.userprospects.any(id=prospect_id)).filter(Prospects.prospectsuser.any(id=user_id)).all()
        prospects_list = list(filter(lambda each: each.id==user_id, prospects_query))
        if not prospects_list:
            specific_prospect.prospectsuser.append(user)
            db.session.commit() 
            return jsonify(input_data),200
        else:
            return jsonify({"msg" : "prospect already created"}),400
    else:   
        db.session.add(new_prospect)
        user.userprospects.append(new_prospect)
        db.session.commit()             
        return jsonify(input_data),200

@app.route('/prospects/<int:user_id>', methods=['GET'])
def get_all_prospects(user_id):
        prospects_query = Prospects.query.filter(Prospects.prospectsuser.any(id=user_id)).all()
        prospects_list = list(map(lambda each: each.serialize(), prospects_query))
        return jsonify(prospects_list), 200


@app.route('/addContact', methods=['POST'])
def addContact():
    input_data = request.json

    prospect_account = Prospects.query.filter_by(
        account=input_data['account']
    ).one_or_none()

    specific_contact = Contacts.query.filter_by(
        first_name=input_data['first_name'],
        last_name=input_data['last_name']
    ).one_or_none()

    if isinstance(specific_contact,Contacts):
        return jsonify({"msg" : "contact already created"}),400
    else:
        new_contact= Contacts(
            first_name = input_data['first_name'],
            last_name = input_data['last_name'],
            position = input_data['position'],
            title = input_data['title'],
            email = input_data['email'],
            phone_number = input_data['phone_number']
        )
        db.session.add(new_contact)
        new_contact.prospectscontacts.append(prospect_account)
        db.session.commit()            
        return jsonify(input_data),200

@app.route('/contacts', methods=['GET'])
def get_all_contacts():
        contacts_query = Contacts.query.all()
        # contacts_query = Contacts.query.filter(Contacts.prospectscontacts.any(id=user_id)).all()
        contacts_list = list(map(lambda each: each.serialize(), contacts_query))
        return jsonify(contacts_list), 200

@app.route('/organizations', methods=['GET'])
def get_all_organizations():
        contacts_query = Organizations.query.all()
        organizations_list = list(map(lambda each: each.serialize(), contacts_query))
        return jsonify(organizations_list), 200



# EBIDA = Earnings Before Interest Depreciation and Amortization
# Net Income + Interest Expense + Depreciation and Amortization Expense
# Current Ratio = Current Assets / Current Liabilities
# function calcCurrentRatio (currentAssets, currentLiabilities){
#   return currentAssets/currentLiabilities;
# }
# function calcWorkingCapital (currentAssets, currentLiabilities){
#   return currentAssets - currentLiabilities;
# }
# Working Capital = Current Assets - Current Liabilities
# Gross Profit = Total REvenue - Cost of Goods Sold (COGS)
# Accounts: Checking Account (DDA), Savings Account (SAV), Money Market (MMK)--- Loans: Revolving Line of Credit (RLOC), Owner-Occupied MTG (OORE MTG mortgage), Equipment Financing


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
