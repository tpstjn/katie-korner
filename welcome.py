#############################
# Welcome to Katie's Korner!
#############################

# region Import/Basic Init

#########
# Imports
#########
import enum

from sqlalchemy.orm import session
from forms.login_forms import EditEmployeeForm, LoginForm, RegisterForm, RegisterEmployeeForm
from security.hashing import UpdatedHasher
import os
import sys
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login.utils import fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, AnonymousUserMixin, login_manager, login_required
from flask_login import login_user, logout_user, current_user
from enum import Flag, auto

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

from security.hashing import UpdatedHasher
from forms.login_forms import LoginForm, RegisterForm
from forms.order_forms import OrderPint, OrderMilkshake, OrderCone, OrderSundae, SchedulePickupForm
# endregion

# region Basic Config

#####################
# Basic Configuration
#####################

# Identify necessary files
dbfile = os.path.join(script_dir, "katie's_korner.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")

# open and read the contents of the pepper file into your pepper key
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()

# create a new instance of UpdatedHasher using that pepper key
pwd_hasher = UpdatedHasher(pepper_key)

# Configure Flask App
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'folgawoogaimogawomp'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['KATIES_ADMIN'] = 'tpstjn@gmail.com'

# Get database object
db = SQLAlchemy(app)

# Prepare and connect LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# endregion

# region Database

class Employee_Role(Flag):
    Cashier = auto()
    Kitchen = auto()
    Cleaner = auto()
    Manager = auto()
    Boss = auto()

##########
# Database
##########

# region Permissions

# Enumerates permissions allowed to various users
class Permission:
    ORDER = 1
    ADD_FLAVOR = 2
    ADMIN = 4

# endregion

# region Role

# Various roles users can have (Customer, Employee, Admin)
class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return (self.permissions & permission == permission)

    # For testing purposes
    @staticmethod
    def insert_roles():
        roles = {
            'Customer': [Permission.ORDER],
            'Employee': [Permission.ORDER, Permission.ADD_FLAVOR],
            'Administrator': [Permission.ORDER, Permission.ADD_FLAVOR, Permission.ADMIN]
        }
        default_role = 'Customer'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
# endregion

# region User

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary)
    # differentiate between different types of users
    user_role = db.Column(db.Integer, db.ForeignKey('Roles.id'))

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")

    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)

    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)

    # If app defines user as admin, make admin
    # Otherwise, set to default (Customer)
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.user_role is None:
            if self.email == app.config['KATIES_ADMIN']:
                self.user_role = Role.query.filter_by(name='Administrator').first().id
        if self.user_role is None:
            self.user_role = Role.query.filter_by(default=True).first().id

    # Define permissions
    def can(self, permission):
        return (self.user_role is not None and self.user_role.has_permission(permission))

    def is_administrator(self):
        return self.can(Permission.ADMIN)
# endregion

# region AnonymousUser


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser

# endregion

# region Flavors


class IceCreamFlavors(db.Model):
    __tablename__ = 'IceCreamFlavors'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Unicode, nullable=False)
    isRegularFlavor = db.Column(db.Boolean, nullable=False)
    isSherbet = db.Column(db.Boolean, nullable=False)
    hasSugar = db.Column(db.Boolean, nullable=False)
    
    @staticmethod
    def insert_flavors():
        flavors = (
            IceCreamFlavors(flavor="Banana", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Black Cherry",
                            isRegularFlavor=True, isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Cotton Candy",
                            isRegularFlavor=True, isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Bubble Gum", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Chocolate", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Blue Boy", isRegularFlavor=False,
                            isSherbet=True, hasSugar=True),
            IceCreamFlavors(flavor="Orange", isRegularFlavor=False,
                            isSherbet=True, hasSugar=True),
            IceCreamFlavors(flavor="Red Raspberry",
                            isRegularFlavor=False, isSherbet=True, hasSugar=True),
            IceCreamFlavors(
                flavor="Cutter Pecan", isRegularFlavor=False, isSherbet=False, hasSugar=False),
            IceCreamFlavors(
                flavor="Fudge Ripple", isRegularFlavor=False, isSherbet=False, hasSugar=False),
            IceCreamFlavors(flavor="Vanilla", isRegularFlavor=False,
                            isSherbet=False, hasSugar=False)
        )
        for f in flavors:
            db.session.add(f)
        db.session.commit()
# endregion

# region Employees

class Employee(db.Model):
    __tablename__ = 'Employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    first_name = db.Column(db.Unicode, nullable=False)
    last_name = db.Column(db.Unicode, nullable=False)
    # differentiate between different types of employees
    employee_role = db.Column(db.Integer)

# endregion 

# endregion

# region ForDebug

# db.drop_all()
db.create_all()  # this is only needed if the database doesn't already exist

# Role.insert_roles()
# IceCreamFlavors.insert_flavors()

# endregion

# region Classes

class PintOrder:
    def __init__(self, flavor, quantity):
        self.flavor = flavor
        self.quantity = quantity

class MilkshakeOrder:
    def __init__(self, flavor, quantity, addWhippedCream, addCherry):
        self.flavor = flavor
        self.quantity = quantity
        self.addWhippedCream = addWhippedCream
        self.addCherry = addCherry

class ConeOrder:
    def __init__(self, flavor, quantity, coneType, numOfScoops):
        self.flavor = flavor
        self.quantity = quantity
        self.coneType = coneType
        self.numOfScoops = numOfScoops

# endregion

# region Route Handlers

################
# Route Handlers
################

# region Home Page

###########
# Home Page
###########
@app.route("/")
def index():
    return render_template('home.j2', user=current_user)

# endregion

# region Login

#######
# Login
#######

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.j2', form=form, user=current_user)

    if request.method == 'POST':
        if form.validate():

            # try to get the user associated with this email address
            # check if user is a Customer
            user = User.query.filter_by(email=form.email.data).first()
            # if user exists and password matches...
            if user is not None and user.verify_password(form.password.data):
                # log this user in through the login_manager
                login_user(user, remember=form.rememberMe.data)
                # redirect the user to the page they wanted or the home page
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('index')
                return redirect(next)
            else:
                flash("Wrong username or password", 'error')
                return redirect(url_for('login'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}", 'error')
            return redirect(url_for('login'))

# endregion

# region Register Customer

###################
# Register Customer
###################


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.j2', form=form, user=current_user)
    if request.method == 'POST':
        if form.validate():
            # Check if email & pwd are in DB
            user = User.query.filter_by(email=form.email.data).first()
            # if the email address is free, create a new user and send to login
            if user is None:
                user = User(email=form.email.data,
                            password=form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully', 'success')
                return redirect(url_for('login'))
            else:  # if user already exists
                # flash warning message and redirect
                flash('There is already an account with that email address', 'error')
                return redirect(url_for('register'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}", 'error')
            return redirect(url_for('register'))

# endregion

# region Logout

########
# Logout
########
@app.get('/logout/')
def get_logout():
    logout_user()
    flash('You have been logged out', 'no-background-success')
    return redirect(url_for('index'))

# endregion

# region Flavors

#########
# Flavors
#########
@app.get('/flavors/')
def flavors():
    # flavorList = IceCreamFlavors.query.all()
    # flavorMessage = ""
    # for flavor in flavorList:
    #     flavorMessage += f"{flavor.flavor} : {flavor.isRegularFlavor} : {flavor.isSherbet} : {flavor.hasSugar}\n"
    # flash(flavorMessage)
    return render_template('flavors.j2', user=current_user, flavorList=IceCreamFlavors.query.all())

# endregion

# region ORDER AHEAD
#############
# Order Ahead
#############
@app.route('/order/schedule/', methods=['GET', 'POST'])
def order_schedule():
    form = SchedulePickupForm()
    if request.method == 'GET':
        return render_template("order_schedule.j2", form=form)
    elif request.method == 'POST':
        if form.validate():
            if form.goBackBut.data:
                return redirect(url_for('index'))
            elif form.continueBut.data:
                return redirect(url_for('order_menu'))
        else:
            flash("Invalid Scheduling Information")
            return redirect(url_for('order_schedule'))

order = list()
@app.route('/order/menu/', methods=["GET", "POST"])
def order_menu():
    #TODO some validation to make sure they've entered in valid data for pickup, and not just routing themselves to the menu
    pintForm = OrderPint()
    milkshakeForm = OrderMilkshake()
    coneForm = OrderCone()
    flavors = IceCreamFlavors.query.all()
    flavor_names = [flavor.flavor for flavor in flavors]
    pintForm.flavor.choices = flavor_names
    milkshakeForm.flavor.choices = flavor_names
    coneForm.flavor.choices = flavor_names
    if request.method == "GET":
        return render_template("order_menu.j2", pintForm=pintForm, milkshakeForm=milkshakeForm, coneForm=coneForm)
    elif request.method == "POST":
        if pintForm.submitOrderPint.data:
            if pintForm.validate():
                inList = False
                for item in order:
                    if item.flavor == pintForm.flavor.data:
                        item.quantity += pintForm.quantity.data
                        inList = True
                if not inList:
                    order.append(PintOrder(pintForm.flavor.data, pintForm.quantity.data))
                for item in order:
                    if isinstance(item, PintOrder):
                        print(f"{item.flavor}: {item.quantity}", file=sys.stderr)
                return redirect(url_for('order_menu'))       
            else:
                for field, error in pintForm.errors.items():
                    flash(f"{field}: {error}")
                return redirect(url_for('order_menu'))
        elif milkshakeForm.submitOrderMilkshake.data:
            inList = False
            for item in order:
                if item.flavor == milkshakeForm.flavor.data:
                    item.quantity += milkshakeForm.quantity.data
                    inList = True
                if not inList:
                    order.append(MilkshakeOrder(milkshakeForm.flavor.data, milkshakeForm.quantity.data, milkshakeForm.addWhippedCream.data, milkshakeForm.addCherry.data))
                for item in order:
                    if isinstance(item, MilkshakeOrder):
                        print(f"{item.flavor}: {item.quantity}, WC:{item.addWhippedCream}, C:{item.addCherry}", file=sys.stderr)
                return redirect(url_for('order_menu'))
            else:
                for field, error in milkshakeForm.errors.items():
                    flash(f"{field}: {error}")
                return redirect(url_for('order_menu'))
        elif coneForm.submitOrderCone.data:
            inList = False
            for item in order:
                if item.flavor == coneForm.flavor.data:
                    item.quantity += coneForm.quantity.data
                    inList = True
                if not inList:
                    order.append(ConeOrder(coneForm.flavor.data, coneForm.quantity.data, coneForm.coneType.data, coneForm.numOfScoops.data))
                for item in order:
                    if isinstance(item, ConeOrder):
                        print(f"{item.flavor}: {item.quantity}, {item.coneType}, {item.numOfScoops}", file=sys.stderr)
                return redirect(url_for('order_menu'))
            else:
                for field, error in coneForm.errors.items():
                    flash(f"{field}: {error}")
                return redirect(url_for('order_menu'))
        if request.form['submit_button'] == 'Checkout':
            # Clear out list to free it up for the next order
            return redirect(url_for("order_checkout"))

@app.route('/order/checkout')
def order_checkout():
    checkout_order = list(order)
    order.clear()
    return render_template("checkout.j2", user=current_user, order=checkout_order)
# endregion

# endregion

# region Admin

##################
# Admin Management
##################
@app.route('/manage/', methods=['GET', 'POST'])
@fresh_login_required
def manage():
    registerForm = RegisterEmployeeForm()
    editForm = EditEmployeeForm()
    roles = [Employee_Role.Cashier, Employee_Role.Kitchen, Employee_Role.Cleaner, Employee_Role.Manager, Employee_Role.Boss]
    registerForm.role.choices = [(role.value, role.name) 
                                for role in roles]
    editForm.role.choices = registerForm.role.choices

    if request.method == 'POST':
        # Edit employee attributes
        if editForm.submitEdit.data:
            id = request.args.get('id')
            db.session.query(Employee).\
                filter(Employee.id == id).\
                update({"employee_role": (editForm.role.data)})
            db.session.commit()
            return redirect(url_for('manage'))
        # Add new employee
        if registerForm.submitRegister.data:
            if registerForm.validate():
                # Check if email & pwd are in DB
                user = User.query.filter_by(email=registerForm.email.data).first()
                # if the email address is free, create a new user and send to login
                if user is None:
                    #Add employee to Users Table
                    user = User(email=registerForm.email.data,
                                password=registerForm.password.data)
                    db.session.add(user)
                    db.session.commit()
                    
                    #Add employee to Employees Table
                    employee = Employee(email=registerForm.email.data,
                                        first_name=registerForm.firstName.data,
                                        last_name=registerForm.lastName.data,
                                        employee_role=registerForm.role.data)
                    db.session.add(employee)
                    db.session.commit()

                    flash('Account created successfully', 'no-background-success')
                    return redirect(url_for('manage'))
                else:  # if user already exists
                    # flash warning message and redirect
                    flash('There is already an account with that email address', 'no-background-warning')
                    return redirect(url_for('manage'))
            else:
                for field, error in registerForm.errors.items():
                    flash(f"{field}: {error}", 'error-employee')

    employees = Employee.query.all()
    return render_template("manage.j2", user=current_user, registerForm=registerForm, editForm=editForm, 
                            employees=employees, roles=roles)

@app.route('/removeEmployee/<int:id>/', methods=['GET', 'DELETE'])
def removeEmployee(id):
    # Remove employee from database
    Employee.query.filter_by(id=id).delete()
    db.session.commit()
    return(redirect(url_for('manage')))

# endregion

# region Geolocation
####################
# GEOLOCATION ROUTE 
####################
@app.route("/map/")
def map():
    return render_template("geolocation.j2", user=current_user)
# endregion