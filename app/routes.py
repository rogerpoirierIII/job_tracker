from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import SignupForm, LoginForm
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

# user sign up route
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please login or use a different email.', 'danger')
            return redirect(url_for('main.signup'))

        # Hash password
        hashed_password = generate_password_hash(form.password.data)

        # Create new user
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)
# user login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)  # Flask-Login
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))  # or wherever
        else:
            flash('Login failed. Check email and password.', 'danger')
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

@main.route('/')
def home():
    # If logged in, go to dashboard, else go to login page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))
