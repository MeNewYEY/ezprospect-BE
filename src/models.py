from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, timezone, datetime
from decimal import Decimal, ROUND_HALF_UP

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
            "phone_number": self.phone_number
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
    lat = db.Column(db.String(250), nullable=False)
    lon = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __init__(self,name,industry,address1,city,state,zipCode,phone_number,account,lat,lon):
        self.name=name
        self.industry=industry
        self.address1=address1
        self.city=city
        self.state=state
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.account=account
        self.lat=lat
        self.lon=lon
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return f'<Prospects {self.id},{self.account}>'

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
            "account": self.account,
            "lat": self.lat,
            "lon": self.lon
            # do not serialize the password, its a security breach
        }

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    position = db.Column(db.String(250), unique=False, nullable=False)
    title = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    prospectscontacts = db.relationship('Prospects', secondary=prospects_contacts, backref=db.backref('prospectscontacts', lazy='dynamic'))
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False) 
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

    def __init__(self,first_name,last_name,position,title,email,phone_number,user_id):
        self.first_name=first_name
        self.last_name=last_name
        self.position=position
        self.title=title
        self.email=email
        self.phone_number=phone_number
        self.user_id=user_id
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
            "phone_number": self.phone_number,
            "user_id": self.user_id,
        }

class BackCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    prospect_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    data = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self,prospect_id,user_id,data):
        self.data=data
        self.prospect_id=prospect_id
        self.user_id=user_id
        self.date=datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<BackCompany %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "data": self.data,
            "prospect_id": self.prospect_id,
            "user_id": self.user_id,
            "date":self.date
            # do not serialize the password, its a security breach
        }

class BackOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    prospect_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    data = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


    def __init__(self,prospect_id,user_id,data):
        self.data=data
        self.prospect_id=prospect_id
        self.user_id=user_id
        self.date=datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<BackOwner %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "data": self.data,
            "prospect_id": self.prospect_id,
            "user_id": self.user_id,
            "date":self.date
            # do not serialize the password, its a security breach
        }


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    status = db.Column(db.Boolean(), unique=False, nullable=False)
   

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

class Financial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prospect_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    statement_date = db.Column(db.DateTime(timezone=True))
    quality = db.Column(db.String(50))
    cash = db.Column(db.Numeric, unique=False, nullable=False)
    accounts_receivable = db.Column(db.Numeric, unique=False, nullable=False)
    raw_materials = db.Column(db.Numeric, unique=False, nullable=False)
    work_in_process = db.Column(db.Numeric, unique=False, nullable=False)
    finished_goods = db.Column(db.Numeric, unique=False, nullable=False)
    total_inventory = db.Column(db.Numeric, unique=False, nullable=False)
    total_current_assets = db.Column(db.Numeric, unique=False, nullable=False)
    land = db.Column(db.Numeric, unique=False, nullable=False)
    construction_in_progress = db.Column(db.Numeric, unique=False, nullable=False)
    buildings = db.Column(db.Numeric, unique=False, nullable=False)
    machines_and_equipment = db.Column(db.Numeric, unique=False, nullable=False)
    furniture_and_fixtures = db.Column(db.Numeric, unique=False, nullable=False)
    vehicles = db.Column(db.Numeric, unique=False, nullable=False)
    leasehold_improvements = db.Column(db.Numeric, unique=False, nullable=False)
    capital_leases = db.Column(db.Numeric, unique=False, nullable=False)
    other_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_gross_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    accumulated_depreciation = db.Column(db.Numeric, unique=False, nullable=False)
    net_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_assets = db.Column(db.Numeric, unique=False, nullable=False)
    goodwill = db.Column(db.Numeric, unique=False, nullable=False)
    other_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    total_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    accumulated_amortization = db.Column(db.Numeric, unique=False, nullable=False)
    net_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    other_non_operating_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_non_current_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_assets = db.Column(db.Numeric, unique=False, nullable=False)
    short_term_debt_secured = db.Column(db.Numeric, unique=False, nullable=False)
    short_term_debt_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    cpltd_secured = db.Column(db.Numeric, unique=False, nullable=False)
    cpltd_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    other_notes_payable = db.Column(db.Numeric, unique=False, nullable=False)
    accounts_payable_trade = db.Column(db.Numeric, unique=False, nullable=False)
    other_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    ltd_secured = db.Column(db.Numeric, unique=False, nullable=False)
    ltd_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    other_lt_notes_payable = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_liaibilities = db.Column(db.Numeric, unique=False, nullable=False)
    other_non_operating_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_non_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    common_stock = db.Column(db.Numeric, unique=False, nullable=False)
    additional_paid_in_capital = db.Column(db.Numeric, unique=False, nullable=False)
    retained_earnings = db.Column(db.Numeric, unique=False, nullable=False)
    total_equity = db.Column(db.Numeric, unique=False, nullable=False)
    liabilities_and_equity = db.Column(db.Numeric, unique=False, nullable=False)
    tangible_net_worth = db.Column(db.Numeric, unique=False, nullable=False)
    working_capital = db.Column(db.Numeric, unique=False, nullable=False)
    current_ratio = db.Column(db.Numeric, unique=False, nullable=False)
    quick_ratio = db.Column(db.Numeric, unique=False, nullable=False)
    leverage = db.Column(db.Numeric, unique=False, nullable=False)
    total_revenue = db.Column(db.Numeric, unique=False, nullable=False)
    total_cogs = db.Column(db.Numeric, unique=False, nullable=False)
    gross_profit = db.Column(db.Numeric, unique=False, nullable=False)
    gpm = db.Column(db.Numeric, unique=False, nullable=False)
    sga_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    rent_expense = db.Column(db.Numeric, unique=False, nullable=False)
    depreciation_expense = db.Column(db.Numeric, unique=False, nullable=False)
    amortization_expense = db.Column(db.Numeric, unique=False, nullable=False)
    bad_debt_expense = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    total_operating_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    total_operating_profit = db.Column(db.Numeric, unique=False, nullable=False)
    operating_profit_margin = db.Column(db.Numeric, unique=False, nullable=False)
    interest_expense = db.Column(db.Numeric, unique=False, nullable=False)
    interest_income = db.Column(db.Numeric, unique=False, nullable=False)
    other_income_expense = db.Column(db.Numeric, unique=False, nullable=False)
    total_other_income_expense = db.Column(db.Numeric, unique=False, nullable=False)
    total_profit_before_taxes = db.Column(db.Numeric, unique=False, nullable=False)
    tax_provision = db.Column(db.Numeric, unique=False, nullable=False)
    net_income = db.Column(db.Numeric, unique=False, nullable=False)
    distributions = db.Column(db.Numeric, unique=False, nullable=False)
    ebida = db.Column(db.Numeric, unique=False, nullable=False)
    ebitda = db.Column(db.Numeric, unique=False, nullable=False)
    ebitdar = db.Column(db.Numeric, unique=False, nullable=False)
    net_profit_margin = db.Column(db.Numeric, unique=False, nullable=False)
    roa = db.Column(db.Numeric, unique=False, nullable=False)
    roe = db.Column(db.Numeric, unique=False, nullable=False)

    def __init__(self,accounts,user_id):
        self.prospect_id = accounts["prospect_id"]
        self.user_id = user_id
        self.statement_date = datetime.strptime(accounts["statement_date"],"%Y-%m-%d")
        self.quality = accounts["quality"]
        self.cash = float(accounts["cash"])
        self.accounts_receivable = float(accounts["accounts_receivable"])
        self.raw_materials = float(accounts["raw_materials"])
        self.work_in_process = float(accounts["work_in_process"])
        self.finished_goods = float(accounts["finished_goods"])
        self.total_inventory = self.calculate_total_inventory(self.raw_materials, self.work_in_process, self.finished_goods)
        self.total_current_assets = self.calculate_total_current_assets(self.cash, self.accounts_receivable, self.total_inventory)
        self.land = float(accounts["land"])
        self.construction_in_progress = float(accounts["construction_in_progress"])
        self.buildings = float(accounts["buildings"])
        self.machines_and_equipment = float(accounts["machines_and_equipment"])
        self.furniture_and_fixtures = float(accounts["furniture_and_fixtures"])
        self.vehicles = float(accounts["vehicles"])
        self.leasehold_improvements = float(accounts["leasehold_improvements"])
        self.capital_leases = float(accounts["capital_leases"])
        self.other_fixed_assets = float(accounts["other_fixed_assets"])
        self.total_gross_fixed_assets = self.calculate_total_gross_fixed_assets(self.land, self.construction_in_progress, self.buildings, self.machines_and_equipment, self.furniture_and_fixtures, self.vehicles, self.leasehold_improvements, self.capital_leases, self.other_fixed_assets)
        self.accumulated_depreciation = float(accounts["accumulated_depreciation"])
        self.net_fixed_assets = self.calculate_net_fixed_assets(self.total_gross_fixed_assets, self.accumulated_depreciation)
        self.other_operating_assets = float(accounts["other_operating_assets"])
        self.goodwill = float(accounts["goodwill"])
        self.other_intangibles = float(accounts["other_intangibles"])
        self.total_intangibles = self.calculate_total_intangibles(self.goodwill, self.other_intangibles)
        self.accumulated_amortization = float(accounts["accumulated_amortization"])
        self.net_intangibles = self.calculate_net_intangibles(self.total_intangibles, self.accumulated_amortization)
        self.other_non_operating_assets = float(accounts["other_non_operating_assets"])
        self.total_non_current_assets = self.calculate_total_non_current_assets(self.net_fixed_assets, self.other_operating_assets, self.net_intangibles, self.other_non_operating_assets)
        self.total_assets = self.calculate_total_assets(self.total_current_assets, self.total_non_current_assets)
        self.short_term_debt_secured = float(accounts["short_term_debt_secured"])
        self.short_term_debt_unsecured = float(accounts["short_term_debt_unsecured"])
        self.cpltd_secured = float(accounts["cpltd_secured"])
        self.cpltd_unsecured = float(accounts["cpltd_unsecured"])
        self.other_notes_payable = float(accounts["other_notes_payable"])
        self.accounts_payable_trade = float(accounts["accounts_payable_trade"])
        self.other_current_liabilities = float(accounts["other_current_liabilities"])
        self.total_current_liabilities = self.calculate_total_current_liabilities(self.short_term_debt_secured, self.short_term_debt_unsecured, self.cpltd_secured, self.cpltd_unsecured, self.other_notes_payable, self.accounts_payable_trade, self.other_current_liabilities)
        self.ltd_secured = float(accounts["ltd_secured"])
        self.ltd_unsecured = float(accounts["ltd_unsecured"])
        self.other_lt_notes_payable = float(accounts["other_lt_notes_payable"])
        self.other_operating_liaibilities = float(accounts["other_operating_liabilities"])
        self.other_non_operating_liabilities = float(accounts["other_non_operating_liabilities"])
        self.total_non_current_liabilities = self.calculate_total_non_current_liabilities(self.ltd_secured, self.ltd_unsecured, self.other_lt_notes_payable)
        self.total_liabilities = self.calculate_total_liabilities(self.total_current_liabilities, self.total_non_current_liabilities)
        self.common_stock = float(accounts["common_stock"])
        self.additional_paid_in_capital = float(accounts["additional_paid_in_capital"])
        self.retained_earnings = float(accounts["retained_earnings"])
        self.total_equity = self.calculate_total_equity(self.common_stock, self.additional_paid_in_capital, self.retained_earnings)
        self.liabilities_and_equity = self.calculate_liabilities_and_equity(self.total_liabilities, self.total_equity)
        self.tangible_net_worth = self.calculate_tangible_net_worth(self.total_equity, self.net_intangibles)
        self.working_capital = self.calculate_working_capital(self.total_current_assets, self.total_current_liabilities)
        self.current_ratio = self.calculate_current_ratio(self.total_current_assets, self.total_current_liabilities)
        self.quick_ratio = self.calculate_quick_ratio(self.total_current_assets, self.total_inventory, self.total_current_liabilities)
        self.leverage = self.calculate_leverage(self.total_liabilities, self.total_equity)
        self.total_revenue = float(accounts["total_revenue"])
        self.total_cogs = float(accounts["total_cogs"])
        self.gross_profit = self.calculate_gross_profit(self.total_revenue, self.total_cogs)
        self.gpm = self.calculate_gpm(self.gross_profit, self.total_revenue)
        self.sga_expenses = float(accounts["sga_expenses"])
        self.rent_expense = float(accounts["rent_expense"])
        self.depreciation_expense = float(accounts["depreciation_expense"])
        self.amortization_expense = float(accounts["amortization_expense"])
        self.bad_debt_expense = float(accounts["bad_debt_expense"])
        self.other_operating_expenses = float(accounts["other_operating_expenses"])
        self.total_operating_expenses = self.calculate_total_operating_expenses(self.sga_expenses, self.rent_expense, self.depreciation_expense, self.amortization_expense, self.bad_debt_expense, self.other_operating_expenses)
        self.total_operating_profit = self.calculate_total_operating_profit(self.gross_profit, self.total_operating_expenses)
        self.operating_profit_margin = self.calculate_operating_profit_margin(self.total_operating_profit, self.total_revenue)
        self.interest_expense = float(accounts["interest_expense"])
        self.interest_income = float(accounts["interest_income"])
        self.other_income_expense = float(accounts["other_income_expense"])
        self.total_other_income_expense = self.calculate_total_other_income_expense(self.interest_expense, self.interest_income, self.other_income_expense)
        self.total_profit_before_taxes = self.calculate_total_profit_before_taxes(self.total_operating_profit, self.total_other_income_expense)
        self.tax_provision = float(accounts["tax_provision"])
        self.net_income = self.calculate_net_income(self.total_profit_before_taxes, self.tax_provision)
        self.net_profit_margin = self.calculate_net_profit_margin(self.net_income, self.total_revenue)
        self.distributions = float(accounts["distributions"])
        self.ebida = self.calculate_ebida(self.net_income, self.interest_expense, self.depreciation_expense, self.amortization_expense)
        self.ebitda = self.calculate_ebitda(self.net_income, self.interest_expense, self.tax_provision, self.depreciation_expense, self.amortization_expense)
        self.ebitdar = self.calculate_ebitdar(self.net_income, self.interest_expense,self.tax_provision, self.depreciation_expense, self.amortization_expense, self.rent_expense)
        self.roa = self.calculate_roa(self.net_income, self.total_assets)
        self.roe = self.calculate_roe(self.net_income, self.total_equity)

    def calculate_total_inventory (self, raw_materials, work_in_process, finished_goods):
        return raw_materials + work_in_process + finished_goods

    def calculate_total_current_assets (self, cash, accounts_receivable, total_inventory):
        return cash + accounts_receivable + total_inventory
    
    def calculate_total_gross_fixed_assets (self, land, construction_in_progress, buildings, machines_and_equipment, furniture_and_fixtures, vehicles, leasehold_improvements, capital_leases, other_fixed_assets):
        return land + construction_in_progress + buildings + machines_and_equipment + furniture_and_fixtures + vehicles + leasehold_improvements + capital_leases+ other_fixed_assets

    def calculate_net_fixed_assets (self, total_gross_fixed_assets, accumulated_depreciation):
        return total_gross_fixed_assets - accumulated_depreciation

    def calculate_total_intangibles (self, goodwill, other_intangibles):
        return goodwill + other_intangibles

    def calculate_net_intangibles (self, total_intangibles, accumulated_amortization):
        return total_intangibles - accumulated_amortization

    def calculate_total_non_current_assets (self, net_fixed_assets, other_operating_assets, net_intangibles, other_non_operating_assets):
        return net_fixed_assets + other_operating_assets + net_intangibles + other_non_operating_assets

    def calculate_total_assets (self, total_current_assets, total_non_current_assets):
        return total_current_assets + total_non_current_assets

    def calculate_total_current_liabilities (self, short_term_debt_secured, short_term_debt_unsecured, cpltd_secured, cpltd_unsecured, other_notes_payable, accounts_payable_trade, other_current_liabilities):
        return short_term_debt_secured + short_term_debt_unsecured + cpltd_secured + cpltd_unsecured + other_notes_payable + accounts_payable_trade + other_current_liabilities

    def calculate_total_non_current_liabilities (self, ltd_secured, ltd_unsecured, other_lt_notes_payable):
        return ltd_secured + ltd_unsecured + other_lt_notes_payable
    
    def calculate_total_liabilities (self, total_current_liabilities, total_non_current_liabilities):
        return total_current_liabilities + total_non_current_liabilities

    def calculate_total_equity (self, common_stock, additional_paid_in_capital, retained_earnings):
        return common_stock + additional_paid_in_capital + retained_earnings

    def calculate_liabilities_and_equity (self, total_liabilities, total_equity):
        return total_liabilities + total_equity

    def calculate_tangible_net_worth (self, total_equity, net_intangibles):
        return total_equity - net_intangibles

    def calculate_working_capital (self, total_current_assets, total_current_liabilities):
        return total_current_assets - total_current_liabilities
    
    def calculate_current_ratio (self, total_current_assets, total_current_liabilities):
        if total_current_liabilities == 0:
            print("Unable to calculate")
            return 0
        else:
            return total_current_assets / total_current_liabilities

    def calculate_quick_ratio (self, total_current_assets, total_inventory, total_current_liabilities):
        if total_current_liabilities == 0:
            print("Unable to calculate")
            return 0
        return (total_current_assets - total_inventory) / total_current_liabilities

    def calculate_leverage (self, total_liabilities, total_equity):
        if total_equity == 0:
            print("Unable to calculate")
            return 0
        else:
            return total_liabilities / total_equity
    
    def calculate_gross_profit (self, total_revenue,total_cogs):
        return total_revenue - total_cogs
        
    def calculate_gpm (self, gross_profit, total_revenue):
        if total_revenue == 0:
            print("Unable to calculate")
            return 0
        return gross_profit / total_revenue

    def calculate_total_operating_expenses (self, sga_expenses, rent_expense, depreciation_expense, amortization_expense, bad_debt_expense, other_operating_expenses):
        return sga_expenses + rent_expense + depreciation_expense + amortization_expense + bad_debt_expense + other_operating_expenses

    def calculate_total_operating_profit (self, gross_profit, total_operating_expenses):
        return gross_profit - total_operating_expenses

    def calculate_operating_profit_margin (self, total_operating_profit, total_revenue):
        return total_operating_profit / total_revenue if total_revenue != 0 else 0

    def calculate_total_other_income_expense (self, interest_expense, interest_income, other_income_expense):
        return interest_expense + interest_income + other_income_expense

    def calculate_total_profit_before_taxes (self, total_operating_profit, total_other_income_expense):
        return total_operating_profit - total_other_income_expense

    def calculate_net_income (self, total_profit_before_taxes, tax_provision):
        return total_profit_before_taxes - tax_provision

    def calculate_net_profit_margin (self, net_income, total_revenue):
        return net_income / total_revenue if total_revenue != 0 else 0

    def calculate_ebida (self, net_income, interest_expense, depreciation_expense, amortization_expense):
        return net_income + interest_expense + depreciation_expense + amortization_expense

    def calculate_ebitda (self, net_income, interest_expense, tax_provision, depreciation_expense, amortization_expense):
        return net_income + interest_expense + tax_provision + depreciation_expense + amortization_expense

    def calculate_ebitdar (self, net_income, interest_expense, tax_provision, depreciation_expense, amortization_expense, rent_expense):
        return net_income + interest_expense + tax_provision + depreciation_expense + amortization_expense + rent_expense
    
    def calculate_roa (self, net_income, total_assets):
        return net_income / total_assets if total_assets != 0 else 0

    def calculate_roe (self, net_income, total_equity):
        return net_income / total_equity if total_equity != 0 else 0

    def __repr__(self):
        return '<Financial %r>' % self.id
    
    def serialize(self):
        return {
            # do not serialize the password, its a security breach
            "prospect_id": self.prospect_id,
            "user_id": self.user_id,
            "statement_date": self.statement_date.strftime("%m/%d/%Y"),
            "quality": self.quality,
            "cash": '{:,}'.format(int(self.cash.to_integral_value(rounding=ROUND_HALF_UP))),
            "accounts_receivable": '{:,}'.format(int(self.accounts_receivable.to_integral_value(rounding=ROUND_HALF_UP))),
            "raw_materials": '{:,}'.format(int(self.raw_materials.to_integral_value(rounding=ROUND_HALF_UP))),
            "work_in_process": '{:,}'.format(int(self.work_in_process.to_integral_value(rounding=ROUND_HALF_UP))),
            "finished_goods": '{:,}'.format(int(self.finished_goods.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_inventory": '{:,}'.format(int(self.total_inventory.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_current_assets": '{:,}'.format(int(self.total_current_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "land": '{:,}'.format(int(self.land.to_integral_value(rounding=ROUND_HALF_UP))),
            "construction_in_progress": '{:,}'.format(int(self.construction_in_progress.to_integral_value(rounding=ROUND_HALF_UP))),
            "buildings": '{:,}'.format(int(self.buildings.to_integral_value(rounding=ROUND_HALF_UP))),
            "machines_and_equipment": '{:,}'.format(int(self.machines_and_equipment.to_integral_value(rounding=ROUND_HALF_UP))),
            "furniture_and_fixtures": '{:,}'.format(int(self.furniture_and_fixtures.to_integral_value(rounding=ROUND_HALF_UP))),
            "vehicles": '{:,}'.format(int(self.vehicles.to_integral_value(rounding=ROUND_HALF_UP))),
            "leasehold_improvements": '{:,}'.format(int(self.leasehold_improvements.to_integral_value(rounding=ROUND_HALF_UP))),
            "capital_leases": '{:,}'.format(int(self.capital_leases.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_fixed_assets": '{:,}'.format(int(self.other_fixed_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_gross_fixed_assets": '{:,}'.format(int(self.total_gross_fixed_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "accumulated_depreciation": '{:,}'.format(int(self.accumulated_depreciation.to_integral_value(rounding=ROUND_HALF_UP))),
            "net_fixed_assets": '{:,}'.format(int(self.net_fixed_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_operating_assets": '{:,}'.format(int(self.other_operating_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "goodwill": '{:,}'.format(int(self.goodwill.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_intangibles": '{:,}'.format(int(self.other_intangibles.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_intangibles": '{:,}'.format(int(self.total_intangibles.to_integral_value(rounding=ROUND_HALF_UP))),
            "accumulated_amortization": '{:,}'.format(int(self.accumulated_amortization.to_integral_value(rounding=ROUND_HALF_UP))),
            "net_intangibles": '{:,}'.format(int(self.net_intangibles.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_non_operating_assets": '{:,}'.format(int(self.other_non_operating_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_non_current_assets": '{:,}'.format(int(self.total_non_current_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_assets": '{:,}'.format(int(self.total_assets.to_integral_value(rounding=ROUND_HALF_UP))),
            "short_term_debt_secured": '{:,}'.format(int(self.short_term_debt_secured.to_integral_value(rounding=ROUND_HALF_UP))),
            "short_term_debt_unsecured": '{:,}'.format(int(self.short_term_debt_unsecured.to_integral_value(rounding=ROUND_HALF_UP))),
            "cpltd_secured": '{:,}'.format(int(self.cpltd_secured.to_integral_value(rounding=ROUND_HALF_UP))),
            "cpltd_unsecured": '{:,}'.format(int(self.cpltd_unsecured.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_notes_payable": '{:,}'.format(int(self.other_notes_payable.to_integral_value(rounding=ROUND_HALF_UP))),
            "accounts_payable_trade": '{:,}'.format(int(self.accounts_payable_trade.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_current_liabilities": '{:,}'.format(int(self.other_current_liabilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_current_liabilities": '{:,}'.format(int(self.total_current_liabilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "ltd_secured": '{:,}'.format(int(self.ltd_secured.to_integral_value(rounding=ROUND_HALF_UP))),
            "ltd_unsecured": '{:,}'.format(int(self.ltd_unsecured.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_lt_notes_payable": '{:,}'.format(int(self.other_lt_notes_payable.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_operating_liabilities": '{:,}'.format(int(self.other_operating_liaibilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_non_operating_liabilities": '{:,}'.format(int(self.other_non_operating_liabilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_non_current_liabilities": '{:,}'.format(int(self.total_non_current_liabilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_liabilities": '{:,}'.format(int(self.total_liabilities.to_integral_value(rounding=ROUND_HALF_UP))),
            "common_stock": '{:,}'.format(int(self.common_stock.to_integral_value(rounding=ROUND_HALF_UP))),
            "additional_paid_in_capital": '{:,}'.format(int(self.additional_paid_in_capital.to_integral_value(rounding=ROUND_HALF_UP))),
            "retained_earnings": '{:,}'.format(int(self.retained_earnings.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_equity": '{:,}'.format(int(self.total_equity.to_integral_value(rounding=ROUND_HALF_UP))),
            "liabilities_and_equity": '{:,}'.format(int(self.liabilities_and_equity.to_integral_value(rounding=ROUND_HALF_UP))),
            "tangible_net_worth": '{:,}'.format(int(self.tangible_net_worth.to_integral_value(rounding=ROUND_HALF_UP))),
            "working_capital": '{:,}'.format(int(self.working_capital.to_integral_value(rounding=ROUND_HALF_UP))),
            "current_ratio": f"{self.current_ratio.quantize(Decimal('1.00'))}X",
            "quick_ratio": f"{self.quick_ratio.quantize(Decimal('1.00'))}X",
            "leverage": f"{self.leverage.quantize(Decimal('1.00'))}X",
            "total_revenue": '{:,}'.format(int(self.total_revenue.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_cogs": '{:,}'.format(int(self.total_cogs.to_integral_value(rounding=ROUND_HALF_UP))),
            "gross_profit": '{:,}'.format(int(self.gross_profit.to_integral_value(rounding=ROUND_HALF_UP))),
            "gpm": f'{self.gpm.quantize(Decimal("1.00"))}%',
            "sga_expenses": '{:,}'.format(int(self.sga_expenses.to_integral_value(rounding=ROUND_HALF_UP))),
            "rent_expense": '{:,}'.format(int(self.rent_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "depreciation_expense": '{:,}'.format(int(self.depreciation_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "amortization_expense": '{:,}'.format(int(self.amortization_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "bad_debt_expense": '{:,}'.format(int(self.bad_debt_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_operating_expenses": '{:,}'.format(int(self.other_operating_expenses.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_operating_expenses": '{:,}'.format(int(self.total_operating_expenses.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_operating_profit": '{:,}'.format(int(self.total_operating_profit.to_integral_value(rounding=ROUND_HALF_UP))),
            "operating_profit_margin": f'{self.operating_profit_margin.quantize(Decimal("1.00"))}%',
            "interest_expense": '{:,}'.format(int(self.interest_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "interest_income": '{:,}'.format(int(self.interest_income.to_integral_value(rounding=ROUND_HALF_UP))),
            "other_income_expense": '{:,}'.format(int(self.other_income_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_other_income_expense": '{:,}'.format(int(self.total_other_income_expense.to_integral_value(rounding=ROUND_HALF_UP))),
            "total_profit_before_taxes": '{:,}'.format(int(self.total_profit_before_taxes.to_integral_value(rounding=ROUND_HALF_UP))),
            "tax_provision": '{:,}'.format(int(self.tax_provision.to_integral_value(rounding=ROUND_HALF_UP))),
            "net_income": '{:,}'.format(int(self.net_income.to_integral_value(rounding=ROUND_HALF_UP))),
            "net_profit_margin": f'{self.net_profit_margin.quantize(Decimal("1.00"))}%',
            "distributions": '{:,}'.format(int(self.distributions.to_integral_value(rounding=ROUND_HALF_UP))),
            "ebida": '{:,}'.format(int(self.ebida.to_integral_value(rounding=ROUND_HALF_UP))),
            "ebitda": '{:,}'.format(int(self.ebitda.to_integral_value(rounding=ROUND_HALF_UP))),
            "ebitdar": '{:,}'.format(int(self.ebitdar.to_integral_value(rounding=ROUND_HALF_UP))),
            "roa": f'{self.roa.quantize(Decimal("1.00"))}%',
            "roe": f'{self.roe.quantize(Decimal("1.00"))}%'
        }
