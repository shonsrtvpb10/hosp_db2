from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm, AddPatientForm
from flask_gravatar import Gravatar
from functools import wraps


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# gravatar needs to be removed too

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    blood_grp = db.Column(db.String(20), nullable=False)
    guardian_contact = db.Column(db.Integer, nullable=False)
    doctor_name = db.Column(db.String(50), nullable=False)
    payment = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html", current_user=current_user)


@app.route("/add", methods=['GET', 'POST'])
@admin_only
def add():
    form = AddPatientForm()
    if form.validate_on_submit():
        new_patient = Patient(
            name=form.name.data,
            email=form.email.data,
            date=form.date.data,
            contact=form.phone.data,
            age=form.age.data,
            description=form.problem.data,
            address=form.address.data,
            profession=form.profession.data,
            blood_grp=form.blood_grp.data,
            guardian_contact=form.sec_contact.data,
            doctor_name=form.doctor_name.data,
            payment=form.transaction.data
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html",  form=form, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            flash("You've already signed up with that email, log in instead?")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("That email does not exist,please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Incorrect Password Entered,Check Again!")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
