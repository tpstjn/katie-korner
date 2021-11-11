from flask import Flask, render_template, url_for, redirect, request, flash

from login_forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


###############
#Route Handlers
###############
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/welcome/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.j2', form=form)
    if request.method == 'POST':
        if form.validate():
            #TODO: check if email & pwd are in DB
            #TODO: build and redirect to main page
            return redirect(url_for("login_success"))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('login'))

@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.j2', form=form)
    if request.method == 'POST':
        if form.validate():
            #TODO: add email & pwd to DB
            #TODO: build and redirect to main page 
            return redirect(url_for(login_success))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('register'))

@app.route("/login_success/")
def login_success():
    return "Login successfull"