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

class Financials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prospect_id = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, primary_key=True)
    statement_date = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.Integer, primary_key=True)
    fye_month = db.Column(db.Integer, primary_key=True)
    fye_day = db.Column(db.Integer, primary_key=True)
    prepared_by = db.Column(db.Integer, primary_key=True)
    cash = db.Column(db.Decimal, unique=False, nullable=False)
    accounts_receivable = db.Column(db.Decimal, unique=False, nullable=False)
    raw_materials = db.Column(db.Decimal, unique=False, nullable=False)
    work_in_process = db.Column(db.Decimal, unique=False, nullable=False)
    finished_goods = db.Column(db.Decimal, unique=False, nullable=False)
    total_inventory = db.Column(db.Decimal, unique=False, nullable=False)
    land = db.Column(db.Decimal, unique=False, nullable=False)
    construction_in_progress = db.Column(db.Decimal, unique=False, nullable=False)
    buildings = db.Column(db.Decimal, unique=False, nullable=False)
    machines_and_equipment = db.Column(db.Decimal, unique=False, nullable=False)
    furniture_and_fixtures = db.Column(db.Decimal, unique=False, nullable=False)
    vehicles = db.Column(db.Decimal, unique=False, nullable=False)
    leashold_improvements = db.Column(db.Decimal, unique=False, nullable=False)
    capital_leases = db.Column(db.Decimal, unique=False, nullable=False)
    other_fixed_assets = db.Column(db.Decimal, unique=False, nullable=False)
    total_gross_fixed_assets = db.Column(db.Decimal, unique=False, nullable=False)
    accumulated_depreciation = db.Column(db.Decimal, unique=False, nullable=False)
    total_net_fixed_assets = db.Column(db.Decimal, unique=False, nullable=False)
    other_operating_assets = db.Column(db.Decimal, unique=False, nullable=False)
    goodwill = db.Column(db.Decimal, unique=False, nullable=False)
    other_intangibles = db.Column(db.Decimal, unique=False, nullable=False)
    total_intangibles = db.Column(db.Decimal, unique=False, nullable=False)
    accumulated_amortization = db.Column(db.Decimal, unique=False, nullable=False)
    net_intangibles = db.Column(db.Decimal, unique=False, nullable=False)
    other_non_operating_assets = db.Column(db.Decimal, unique=False, nullable=False)
    total_non_current_assets = db.Column(db.Decimal, unique=False, nullable=False)
    total_assets = db.Column(db.Decimal, unique=False, nullable=False)
    short_term_debt_secured = db.Column(db.Decimal, unique=False, nullable=False)
    short_term_debt_unsecured = db.Column(db.Decimal, unique=False, nullable=False)
    cpltd_secured = db.Column(db.Decimal, unique=False, nullable=False)
    cpltd_unsecured = db.Column(db.Decimal, unique=False, nullable=False)
    other_notes_payable = db.Column(db.Decimal, unique=False, nullable=False)
    accounts_payable_trade = db.Column(db.Decimal, unique=False, nullable=False)
    other_current_liabilities = db.Column(db.Decimal, unique=False, nullable=False)
    total_current_liaibilities = db.Column(db.Decimal, unique=False, nullable=False)
    ltd_secured = db.Column(db.Decimal, unique=False, nullable=False)
    ltd_unsecured = db.Column(db.Decimal, unique=False, nullable=False)
    other_lt_notes_payable = db.Column(db.Decimal, unique=False, nullable=False)
    other_operating_liaibilities = db.Column(db.Decimal, unique=False, nullable=False)
    other_non_operating_liabilities = db.Column(db.Decimal, unique=False, nullable=False)
    total_non_current_liabilities = db.Column(db.Decimal, unique=False, nullable=False)
    total_liabilities = db.Column(db.Decimal, unique=False, nullable=False)
    common_stock = db.Column(db.Decimal, unique=False, nullable=False)
    additional_paid_in_capital = db.Column(db.Decimal, unique=False, nullable=False)
    retained_earnings = db.Column(db.Decimal, unique=False, nullable=False)
    total_equity = db.Column(db.Decimal, unique=False, nullable=False)
    tangible_net_worth = db.Column(db.Decimal, unique=False, nullable=False)
    working_capital = db.Column(db.Decimal, unique=False, nullable=False)
    current_ratio = db.Column(db.Decimal, unique=False, nullable=False)
    quick_ratio = db.Column(db.Decimal, unique=False, nullable=False)
    leverage = db.Column(db.Decimal, unique=False, nullable=False)
    total_revenue = db.Column(db.Decimal, unique=False, nullable=False)
    total_cogs = db.Column(db.Decimal, unique=False, nullable=False)
    gross_profit = db.Column(db.Decimal, unique=False, nullable=False)
    gpm = db.Column(db.Decimal, unique=False, nullable=False)
    sga_expenses = db.Column(db.Decimal, unique=False, nullable=False)
    rent_expense = db.Column(db.Decimal, unique=False, nullable=False)
    depreciation_expense = db.Column(db.Decimal, unique=False, nullable=False)
    amortization_expense = db.Column(db.Decimal, unique=False, nullable=False)
    bad_debt_expense = db.Column(db.Decimal, unique=False, nullable=False)
    other_operating_expenses = db.Column(db.Decimal, unique=False, nullable=False)
    total_operating_expenses = db.Column(db.Decimal, unique=False, nullable=False)
    total_operating_profit = db.Column(db.Decimal, unique=False, nullable=False)
    interest_expense = db.Column(db.Decimal, unique=False, nullable=False)
    interest_income = db.Column(db.Decimal, unique=False, nullable=False)
    other_non_operating_income_expense = db.Column(db.Decimal, unique=False, nullable=False)
    total_non_operating_income_expense = db.Column(db.Decimal, unique=False, nullable=False)
    total_profit_before_taxes = db.Column(db.Decimal, unique=False, nullable=False)
    tax_provision = db.Column(db.Decimal, unique=False, nullable=False)
    net_income = db.Column(db.Decimal, unique=False, nullable=False)
    distributions = db.Column(db.Decimal, unique=False, nullable=False)
    ebida = db.Column(db.Decimal, unique=False, nullable=False)
    ebitda = db.Column(db.Decimal, unique=False, nullable=False)
    operating_profit_margin = db.Column(db.Decimal, unique=False, nullable=False)
    net_profit_margin = db.Column(db.Decimal, unique=False, nullable=False)
    roa = db.Column(db.Decimal, unique=False, nullable=False)
    roe = db.Column(db.Decimal, unique=False, nullable=False)

    def __init__(self,accounts):
        self.prospect_id = accounts["prospect_id"]
        self.user_id = accounts["user_id"]
        self.statement_date = accounts["statement_date"]
        self.quality = accounts["quality"]
        self.fye_month = accounts["fye_month"]
        self.fye_day = accounts["fye_day"]
        self.prepared_by = accounts["prepared_by"]
        self.cash = accounts["cash"]
        self.accounts_receivable = accounts["accounts_receivable"]
        self.raw_materials = accounts["raw_materials"]
        self.work_in_process = accounts["work_in_process"]
        self.finished_goods = accounts["finished_goods"]
        self.total_inventory = self.calculate_total_inventory(accounts["raw_materials"], accounts["work_in_process"], accounts["finished_goods"])
        self.land = accounts["land"]
        self.construction_in_progress = accounts["construction_in_progress"]
        self.buildings = accounts["buildings"]
        self.machines_and_equipment = accounts["machines_and_equipment"]
        self.furniture_and_fixtures = accounts["furniture_and_fixtures"]
        self.vehicles = accounts["vehicles"]
        self.leasehold_improvements = accounts["leasehold_improvements"]
        self.capital_leases = accounts["capital_leases"]
        self.other_fixed_assets = accounts["other_fixed_assets"]
        # self.total_gross_fixed_assets = accounts["column"]
        self.accumulated_depreciation = accounts["accumulated_depreciation"]
        self.net_fixed_assets = self.calculate_net_fixed_assets(accounts["column"]
        self.other_operating_assets = accounts["other_operating_assets"]
        self.goodwill = accounts["goodwill"]
        self.other_intangibles = accounts["other_intangibles"]
        # self.total_intangibles = accounts["column"]
        self.accumulated_amortization = accounts["accumulated_amortization"]
        # self.net_intangibles = accounts["column"]
        self.other_non_operating_assets = accounts["other_non_operating_assets"]
        # self.total_non_current_assets = accounts["column"]
        # self.total_assets = accounts["column"]
        self.short_term_debt_secured = accounts["short_term_debt_secured"]
        self.short_term_debt_unsecured = accounts["short_term_debt_unsecured"]
        self.cpltd_secured = accounts["cpltd_secured"]
        self.cpltd_unsecured = accounts["cpltd_unsecured"]
        self.other_notes_payable = accounts["other_notes_payable"]
        self.accounts_payable_trade = accounts["accounts_payable_trade"]
        self.other_current_liabilities = accounts["other_current_liabilities"]
        # self.total_current_liaibilities = accounts["column"]
        self.ltd_secured = accounts["ltd_secured"]
        self.ltd_unsecured = accounts["ltd_unsecured"]
        self.other_lt_notes_payable = accounts["other_lt_notes_payable"]
        self.other_operating_liaibilities = accounts["other_operating_liabilities"]
        self.other_non_operating_liabilities = accounts["other_non_operating_liabilities"]
        # self.total_non_current_liabilities = accounts["column"]
        # self.total_liabilities = accounts["column"]
        self.common_stock = accounts["common_stock"]
        self.additional_paid_in_capital = accounts["additional_paid_in_capital"]
        self.retained_earnings = accounts["retained_earnings"]
        # self.total_equity = accounts["column"]
        # self.tangible_net_worth = accounts["column"]
        # self.working_capital = accounts["column"]
        # self.current_ratio = accounts["column"]
        # self.quick_ratio = accounts["column"]
        # self.leverage = accounts["column"]
        self.total_revenue = accounts["total_revenue"]
        self.total_cogs = accounts["total_cogs"]
        self.gross_profit = self.calculate_gross_profit(accounts["total_revenues"], accounts["total_cogs"])
        # self.gpm = accounts["column"]
        self.sga_expenses = accounts["sga_expenses"]
        self.rent_expense = accounts["rent_expense"]
        self.depreciation_expense = accounts["depreciation_expense"]
        self.amortization_expense = accounts["amortization_expense"]
        self.bad_debt_expense = accounts["bad_debt_expense"]
        self.other_operating_expenses = accounts["other_operating_expenses"]
        # self.total_operating_expenses = accounts["column"]
        # self.total_operating_profit = accounts["column"]
        # self.operating_profit_margin = accounts["column"]
        self.interest_expense = accounts["interest_expense"]
        self.interest_income = accounts["interest_income"]
        self.other_non_operating_income_expense = accounts["other_non_operating_income_expense"]
        # self.total_non_operating_income_expense = accounts["column"]
        # self.total_profit_before_taxes = accounts["column"]
        self.tax_provision = accounts["tax_provision"]
        # self.net_income = accounts["net_income"]
        # self.net_profit_margin = accounts["column"]
        self.distributions = accounts["distributions"]
        # self.ebida = accounts["column"]
        # self.ebitda = accounts["column"]
        # self.roa = accounts["column"]
        # self.roe = accounts["column"]

    def calculate_total_inventory (self, raw_materials, work_in_process, finished_goods):
        return raw_materials + work_in_process + finished_goods
    
    def calculate_total_gross_fixed_assets (self, land, construction_in_progress, buildings, machines_and_equipment, furniture_and_fixtures, vehicles, leasehold_improvements, capital_leases, other_fixed_assets)
        return land + construction_in_progress + buildings + machines_and_equipment + furniture_and_fixtures + vehicles + leasehold_improvements + capital_leases+ other_fixed_assets

    def calculate_net_fixed_assets (self, calculate_total_gross_fixed_assets, accumulated_depreciation)
        return calculate_total_gross_fixed_assets() - accumulated_depreciation

    def calculate_gross_profit (self, total_revenues,total_cogs):
        return total_revenue - total_cogs
        