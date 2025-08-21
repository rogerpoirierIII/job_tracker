from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignupForm, LoginForm
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

# user sign up route
@main.route('/signup', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():  # if the form was successfully submitted
        # Create new user object
        user = User(username=form.username.data, email=form.email.data)
        # Hash and store the password
        user.set_password(form.password.data)
        # Save new user to database
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# user login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Look for the user in the database
        user = User.query.filter_by(email=form.email.data).first()
        # If user exists and password is correct
        if user and user.check_password(form.password.data):
            login_user(user)  # log them in
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# user logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()  # end session
    return redirect(url_for('main.login'))

# Dashboard (only accessible when logged in)
@main.route('/dashboard')
@login_required
def dashboard():
    jobs = current_user.jobs
    return render_template('dashboard.html', jobs=jobs)
