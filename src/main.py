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
from datetime import date, time, datetime
from models import db, User, Prospects, Contacts, Financial,BackOwner, BackCompany
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
                "user_id": specific_user.id,
                "user_name":specific_user.first_name
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

    
    specific_user = User.query.filter_by(
        email=input_data['email']
    ).one_or_none()


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
        
        db.session.add(new_user)
        try:
            db.session.commit()
            response={
                "jwt" : create_jwt(identity=new_user.id),
                "user_id": new_user.id,
                "user_name":new_user.first_name
            }
            return jsonify(response),200

        except Exception as error:
            db.session.rollback()
            return jsonify({"msg" : error}),500

@app.route('/user', methods=['GET'])
@jwt_required
def getUser():
    input_data = request.json
    specific_user_id = get_jwt_identity()
    specific_user = User.query.filter_by(
        id = specific_user_id
        ).one_or_none()

    if specific_user is None:
        return jsonify({"msg" : "user not found"}),404

    else:
        return jsonify(specific_user.serialize()),200

@app.route('/editUser', methods=['POST'])
@jwt_required
def editUser():
    input_data = request.json
    user_id = get_jwt_identity()    
    user=User.query.get(user_id)
    user.phone_number=input_data["phone_number"]
    db.session.commit()
    return jsonify(user.serialize()),200

@app.route('/addProspect', methods=['POST'])
@jwt_required
def add_prospect():
    input_data = request.json
    user_id = get_jwt_identity()

    new_prospect= Prospects(
        name = input_data['name'],
        industry = input_data['industry'],
        address1 = input_data['address1'],
        city = input_data['city'],
        state = input_data['state'],
        zipCode = input_data['zipCode'],
        phone_number = input_data['phone_number'],
        lat = input_data['lat'],
        lon = input_data['lon'],
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
            return jsonify(specific_prospect.serialize()),200
        else:
            return jsonify({"msg" : "prospect already created"}),400
    else:
        db.session.add(new_prospect)       
        user.userprospects.append(new_prospect)           
        db.session.commit()
        return jsonify(new_prospect.serialize()),200

@app.route('/prospects/<int:user_id>', methods=['GET'])
def get_all_prospects(user_id):
    prospects_query = Prospects.query.filter(Prospects.prospectsuser.any(id=user_id)).all()
    prospects_list = list(map(lambda each: each.serialize(), prospects_query))
    return jsonify(prospects_list), 200

    
@app.route('/addBack_company', methods=['POST'])
@jwt_required
def addBackground_Company():
    input_data = request.json
    prospect_id = input_data['prospect_id']
    user_id = get_jwt_identity()
    # user_id=input_data['user_id']

    spec_bakground = BackCompany.query.filter_by(prospect_id=prospect_id,user_id=user_id).first()    

    if(not spec_bakground):
        background = BackCompany(
            prospect_id = prospect_id,
            user_id = user_id,
            data = input_data['data']         
        )
        db.session.add(background)
        db.session.commit()
        return jsonify(background.serialize()),200 
    else:   
        spec_bakground.data = input_data['data']
        spec_bakground.date = datetime.now()
        db.session.commit()
        return jsonify(spec_bakground.serialize()),200

@app.route('/addBack_owner', methods=['POST'])
@jwt_required
def addBackground_Owner():
    input_data = request.json
    prospect_id = input_data['prospect_id']
    user_id = get_jwt_identity()
    # user_id=input_data['user_id']

    spec_bakground = BackOwner.query.filter_by(prospect_id=prospect_id,user_id=user_id).first() 

    if(not spec_bakground):
        background = BackOwner(
            prospect_id = prospect_id,
            user_id = user_id,
            data = input_data['data']         
        )
        db.session.add(background)
        db.session.commit()
        return jsonify(background.serialize()),200
    else:
        spec_bakground.data = input_data['data']
        spec_bakground.date = datetime.now() 
        db.session.commit()       
        return jsonify(spec_bakground.serialize()),200
    


@app.route('/backCompany/<int:user_id>/<int:prospect_id>', methods=['GET'])
def get_background_Company(user_id,prospect_id):
    specific_background = BackCompany.query.filter_by(
        user_id=user_id,prospect_id=prospect_id
    ).one_or_none()
    if (not specific_background):
        background = ""
        return background.serialize(),200
    else:
        return specific_background.serialize(), 200


@app.route('/backOwner/<int:user_id>/<int:prospect_id>', methods=['GET'])
def get_background_Owner(user_id,prospect_id):
    specific_background = BackOwner.query.filter_by(
        user_id=user_id,prospect_id=prospect_id
    ).one_or_none()
    if (not specific_background):
        background = ""
        return background.serialize(),200
    else:
        return specific_background.serialize(), 200


@app.route('/addContact', methods=['POST'])
def addContact():
    input_data = request.json
    user_id = input_data['user_id']

    prospect_account = Prospects.query.filter_by(
        id=input_data['prospect_id']
    ).one_or_none()

    contacts_query = Contacts.query.filter(Contacts.prospectscontacts.any(id=prospect_account.id)).filter_by(user_id=user_id).filter_by(
        first_name=input_data['first_name'],
        last_name=input_data['last_name']
    ).all()

    prospects_list = list(map(lambda each: each.serialize(), contacts_query))  

    if (prospects_list!=[]):
        return jsonify({"msg" : "Contact already created"}),400
    else:
        new_contact= Contacts(
            first_name = input_data['first_name'],
            last_name = input_data['last_name'],
            position = input_data['position'],
            title = input_data['title'],
            email = input_data['email'],
            phone_number = input_data['phone_number'],
            user_id = input_data['user_id']
        )
        db.session.add(new_contact)
        new_contact.prospectscontacts.append(prospect_account)
        db.session.commit() 
        return jsonify(input_data),200

@app.route('/editContact', methods=['PUT'])
def editContact():
    input_data = request.json
    contact = Contacts.query.get(input_data["contact_id"])
    contact.first_name=input_data["first_name"]
    contact.last_name=input_data["last_name"]
    contact.position=input_data["position"]
    contact.title=input_data["title"]
    contact.email=input_data["email"]
    contact.phone_number=input_data["phone_number"]
    db.session.commit()
    return contact.serialize()

@app.route('/deleteContact/<int:id>', methods=['DELETE'])
def delete_Contact(id):
    contact = Contacts.query.get(id)
    if contact is None:
        raise APIException('Statement not found', status_code=404)
    db.session.delete(contact)
    db.session.commit()
    return "ok", 200

@app.route('/contacts/<int:user_id>/<int:prospect_id>', methods=['GET'])
def get_all_contacts(user_id,prospect_id):
    contacts_query = Contacts.query.filter(Contacts.prospectscontacts.any(id=prospect_id)).filter_by(user_id=user_id).all()
    contacts_list = list(map(lambda each: each.serialize(), contacts_query))
    return jsonify(contacts_list), 200

@app.route('/financials', methods=['POST'])
@jwt_required
def save_financials():
    input_data = request.json
    user_id = get_jwt_identity()
    # user_id = input_data["user_id"]

    if 'cash' not in input_data or input_data['cash'] == "":
        input_data['cash'] = 0

    if 'accounts_receivable' not in input_data or input_data['accounts_receivable'] == "":
        input_data['accounts_receivable'] = 0

    if 'raw_materials' not in input_data or input_data['raw_materials'] == "":
        input_data['raw_materials'] = 0

    if 'work_in_process' not in input_data or input_data['work_in_process'] == "":
        input_data['work_in_process'] = 0

    if 'finished_goods' not in input_data or input_data['finished_goods'] == "":
        input_data['finished_goods'] = 0

    if 'land' not in input_data or input_data['land'] == "":
        input_data['land'] = 0
    
    if 'construction_in_progress' not in input_data or input_data['construction_in_progress'] == "":
        input_data['construction_in_progress'] = 0

    if 'buildings' not in input_data or input_data['buildings'] == "":
        input_data['buildings'] = 0

    if 'machines_and_equipment' not in input_data or input_data['machines_and_equipment'] == "":
        input_data['machines_and_equipment'] = 0

    if 'furniture_and_fixtures' not in input_data or input_data['furniture_and_fixtures'] == "":
        input_data['furniture_and_fixtures'] = 0
    
    if 'vehicles' not in input_data or input_data['vehicles'] == "":
        input_data['vehicles'] = 0

    if 'leasehold_improvements' not in input_data or input_data['leasehold_improvements'] == "":
        input_data['leasehold_improvements'] = 0

    if 'capital_leases' not in input_data or input_data['capital_leases'] == "":
        input_data['capital_leases'] = 0

    if 'other_fixed_assets' not in input_data or input_data['other_fixed_assets'] == "":
        input_data['other_fixed_assets'] = 0
    
    if 'accumulated_depreciation' not in input_data or input_data['accumulated_depreciation'] == "":
        input_data['accumulated_depreciation'] = 0

    if 'other_operating_assets' not in input_data or input_data['other_operating_assets'] == "":
        input_data['other_operating_assets'] = 0

    if 'goodwill' not in input_data or input_data['goodwill'] == "":
        input_data['goodwill'] = 0

    if 'other_intangibles' not in input_data or input_data['other_intangibles'] == "":
        input_data['other_intangibles'] = 0
    
    if 'accumulated_amortization' not in input_data or input_data['accumulated_amortization'] == "":
        input_data['accumulated_amortization'] = 0

    if 'other_non_operating_assets' not in input_data or input_data['other_non_operating_assets'] == "":
        input_data['other_non_operating_assets'] = 0
    
    if 'short_term_debt_secured' not in input_data or input_data['short_term_debt_secured'] == "":
        input_data['short_term_debt_secured'] = 0

    if 'short_term_debt_unsecured' not in input_data or input_data['short_term_debt_unsecured'] == "":
        input_data['short_term_debt_unsecured'] = 0

    if 'cpltd_secured' not in input_data or input_data['cpltd_secured'] == "":
        input_data['cpltd_secured'] = 0

    if 'cpltd_unsecured' not in input_data or input_data['cpltd_unsecured'] == "":
        input_data['cpltd_unsecured'] = 0
    
    if 'other_notes_payable' not in input_data or input_data['other_notes_payable'] == "":
        input_data['other_notes_payable'] = 0

    if 'accounts_payable_trade' not in input_data or input_data['accounts_payable_trade'] == "":
        input_data['accounts_payable_trade'] = 0 

    if 'other_current_liabilities' not in input_data or input_data['other_current_liabilities'] == "":
        input_data['other_current_liabilities'] = 0

    if 'ltd_secured' not in input_data or input_data['ltd_secured'] == "":
        input_data['ltd_secured'] = 0

    if 'ltd_unsecured' not in input_data or input_data['ltd_unsecured'] == "":
        input_data['ltd_unsecured'] = 0

    if 'other_lt_notes_payable' not in input_data or input_data['other_lt_notes_payable'] == "":
        input_data['other_lt_notes_payable'] = 0
    
    if 'other_operating_liabilities' not in input_data or input_data['other_operating_liabilities'] == "":
        input_data['other_operating_liabilities'] = 0

    if 'other_non_operating_liabilities' not in input_data or input_data['other_non_operating_liabilities'] == "":
        input_data['other_non_operating_liabilities'] = 0
    
    if 'common_stock' not in input_data or input_data['common_stock'] == "":
        input_data['common_stock'] = 0

    if 'additional_paid_in_capital' not in input_data or input_data['additional_paid_in_capital'] == "":
        input_data['additional_paid_in_capital'] = 0

    if 'retained_earnings' not in input_data or input_data['retained_earnings'] == "":
        input_data['retained_earnings'] = 0

    if 'total_revenue' not in input_data or input_data['total_revenue'] == "":
        input_data['total_revenue'] = 0
    
    if 'total_cogs' not in input_data or input_data['total_cogs'] == "":
        input_data['total_cogs'] = 0

    if 'sga_expenses' not in input_data or input_data['sga_expenses'] == "":
        input_data['sga_expenses'] = 0 

    if 'rent_expense' not in input_data or input_data['rent_expense'] == "":
        input_data['rent_expense'] = 0

    if 'depreciation_expense' not in input_data or input_data['depreciation_expense'] == "":
        input_data['depreciation_expense'] = 0

    if 'amortization_expense' not in input_data or input_data['amortization_expense'] == "":
        input_data['amortization_expense'] = 0
    
    if 'bad_debt_expense' not in input_data or input_data['bad_debt_expense'] == "":
        input_data['bad_debt_expense'] = 0

    if 'other_operating_expenses' not in input_data or input_data['other_operating_expenses'] == "":
        input_data['other_operating_expenses'] = 0 

    if 'interest_expense' not in input_data or input_data['interest_expense'] == "":
        input_data['interest_expense'] = 0

    if 'interest_income' not in input_data or input_data['interest_income'] == "":
        input_data['interest_income'] = 0

    if 'other_income_expense' not in input_data or input_data['other_income_expense'] == "":
        input_data['other_income_expense'] = 0
    
    if 'tax_provision' not in input_data or input_data['tax_provision'] == "":
        input_data['tax_provision'] = 0

    if 'distributions' not in input_data or input_data['distributions'] == "":
        input_data['distributions'] = 0
    print(input_data)
    if 'statement_date' in input_data and 'quality' in input_data:
        new_financial = Financial(
            accounts=input_data,
            user_id = user_id
        )
        db.session.add(new_financial)
        # You will have to format the following code accordingly
        try:
            db.session.commit()
            # the response dictionary needs to be worked - maybe serialize the values of new_financial to give the values they want?

            # response={
            #     'financial' : new_financial.serialize()
            # }
            return jsonify(new_financial.serialize()),200

        except Exception as error:
            db.session.rollback()
            # don't forget to set the error value
            return jsonify({"msg" : error.args}),500
    else:
        return jsonify({"msg" : "information required missing"}),400    
    
    # Do Validation
    # Make sure to check all required columns are set
    # look at line 80
    # And make sure you assign user_id to input_data['user_id']

@app.route('/financials/<int:prospect_id>/<int:user_id>', methods=['GET'])
# @jwt_required
def getStatements(prospect_id,user_id):
    # user_id = get_jwt_identity() 
    user_id = user_id
    statement_query = Financial.query.filter_by(
        user_id = user_id,
        prospect_id=prospect_id
    ).all()
    if(not statement_query):
        return jsonify({"msg" : "Financial statement no created "})
    else:
        dictionary_list = [f.serialize() for f in statement_query]
        print(dictionary_list[0])
        return jsonify(dictionary_list), 200


@app.route('/financials/<int:id>', methods=['DELETE'])
def deleteStatement(id):
    statement = Financial.query.get(id)
    if statement is None:
        raise APIException('Statement not found', status_code=404)
    db.session.delete(statement)
    db.session.commit()
    return "ok", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
