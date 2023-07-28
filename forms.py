from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired, URL


class RegisterForm(FlaskForm):
    email = StringField("Email:-", validators=[DataRequired()])
    password = PasswordField("Password:-", validators=[DataRequired()])
    name = StringField("Name :-", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email :-", validators=[DataRequired()])
    password = PasswordField("Password :-", validators=[DataRequired()])
    submit = SubmitField("Let Me In :-")


class AddPatientForm(FlaskForm):
    name = StringField("Enter Patient's Name- ", validators=[DataRequired()])
    age = StringField("Enter Patient's Age- ", validators=[DataRequired()])
    blood_grp = StringField("Enter Patient's  Blood Group-", validators=[DataRequired()])
    email = StringField("Enter Patient's Email- ", validators=[DataRequired()])
    date = StringField("Enter Date- (in yyyy-mm-dd)", validators=[DataRequired()])
    phone = IntegerField("Enter Contact No.-", validators=[DataRequired()])
    problem = StringField("Problem (Disease)-", validators=[DataRequired()])
    address = StringField("Address of the Patient- ", validators=[DataRequired()])
    profession = StringField("Enter Patient's Profession-", validators=[DataRequired()])
    sec_contact = IntegerField("Enter Partner's Phone No.-", validators=[DataRequired()])
    doctor_name = StringField("Enter Doctor's Name- ", validators=[DataRequired()])
    transaction = StringField("Enter the mode of Payment- ", validators=[DataRequired()])
    submit = SubmitField("Submit Details ->")
