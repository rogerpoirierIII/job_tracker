from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, URL


#Signup form for new users
class SignupForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired()])      # field cannot be empty
    email = StringField('Email', validators=[DataRequired(), Email()]) # field cannot be empty
    password = PasswordField('Password', validators=[DataRequired()])  # field cannot be empty
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]  # confirm password must match password field
    )
    submit = SubmitField('Register')  # button to submit the form

#Login form for existing users to log in
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class JobForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    status = SelectField("Status", choices=[("Applied","Applied"),("Interview","Interview"),("Offer","Offer"),("Rejected","Rejected")])
    website = StringField("Website")
    location = StringField("Location")
    contact = StringField("Contact")
    salary = StringField("Salary")
    notes = TextAreaField("Notes")
    submit = SubmitField("Save")
