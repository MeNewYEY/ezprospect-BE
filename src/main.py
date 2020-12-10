"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from flask_jwt_simple import (JWTManager, jwt_required, create_jwt, get_jwt_identity)
from passlib.hash import sha256_crypt


#from models import Person

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
            return jsonify({"msg" : "Bad credentials"}),400

    else:
        return jsonify({"msg" : "User not found"}),400


@app.route('/signup', methods=['POST'])
def handle_signup():
    input_data = request.json

    if 'email' in input_data and 'password' in input_data:

        specific_user = User.query.filter_by(
            email=input_data['email']
        ).one_or_none()

        if isinstance(specific_user,User):
            return jsonify({"msg" : "email already in use"}),400
        else:
            new_user= User(
                email = input_data['email'],
                password = sha256_crypt.encrypt(str(input_data['password']))
            )

            db.session.add(new_user)
            try:
                db.session.commit()
                return jsonify(new_user.serialize()),200

            except Exception as error:
                db.session.rollback()
                return jsonify({"msg" : error}),500

    else:
        return jsonify({"msg" : "email and password required"}),400

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
