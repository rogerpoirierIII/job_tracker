from alembic.util import status
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import SignupForm, LoginForm, JobForm
from .models import User, db, Job
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
    status_filter = request.args.get('status')
    sort_option = request.args.get('sort')
    search_query = request.args.get('search')

    query = Job.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(
            (Job.title.ilike(f"%{search_query}%")) |
            (Job.company.ilike(f"%{search_query}%"))
        )

    if status_filter:
        query = query.filter_by(status=status_filter)

    if sort_option == "oldest":
        query = query.order_by(Job.created_at.asc())
    elif sort_option == "company":
        query = query.order_by(Job.company.asc())
    elif sort_option == "status":
        query = query.order_by(Job.status.asc())
    else:
        query = query.order_by(Job.created_at.desc())

    jobs = query.all()

    return render_template(
        "dashboard.html",
        jobs=jobs,
        status_filter=status_filter,
        sort_option=sort_option,
        search_query=search_query
    )
# Search / filter / sort endpoint for AJAX
@main.route('/search_jobs')
@login_required
def search_jobs():
    status_filter = request.args.get('status')   # e.g. ?status=Applied
    sort_option = request.args.get('sort')       # newest, oldest, company, status
    search_query = request.args.get('search')    # search term

    query = Job.query.filter_by(user_id=current_user.id)

    # Apply search
    if search_query:
        query = query.filter(
            (Job.title.ilike(f"%{search_query}%")) |
            (Job.company.ilike(f"%{search_query}%"))
        )

    # Apply status filter
    if status_filter:
        query = query.filter_by(status=status_filter)

    # Apply sorting
    if sort_option == "oldest":
        query = query.order_by(Job.created_at.asc())
    elif sort_option == "company":
        query = query.order_by(Job.company.asc())
    elif sort_option == "status":
        query = query.order_by(Job.status.asc())
    else:  # default newest
        query = query.order_by(Job.created_at.desc())

    jobs = query.all()

    # Render only the job cards
    return render_template("job_cards.html", jobs=jobs)

@main.route("/job/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data,
                  company=form.company.data,
                  status=form.status.data,
                  website = form.website.data,
                  location = form.location.data,
                  contact = form.contact.data,
                  salary = form.salary.data,
                  notes=form.notes.data,
                  owner=current_user)
        db.session.add(job)
        db.session.commit()
        flash("Job added successfully!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("job_form.html", form=form)

@main.route("/job/<int:job_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.owner != current_user:
        flash("You do not have permission to edit this job.", "danger")
        return redirect(url_for("main.dashboard"))

    form = JobForm(obj=job)
    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.status = form.status.data
        website = form.website.data
        if website and '://' not in website:
            website = 'https://' + website
        job.website = website
        job.location = form.location.data
        job.contact = form.contact.data
        job.salary = form.salary.data
        job.notes = form.notes.data
        db.session.commit()
        flash("Job updated!", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("job_form.html", form=form)

@main.route("/job/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.owner != current_user:
        flash("You do not have permission to delete this job.", "danger")
        return redirect(url_for("main.dashboard"))

    db.session.delete(job)
    db.session.commit()
    flash("Job deleted!", "success")
    return redirect(url_for("main.dashboard"))
@main.route("/job/<int:job_id>")
@login_required
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    if job.owner != current_user:
        flash("You do not have permission to view this job.", "danger")
        return redirect(url_for("main.dashboard"))
    return render_template("job_details.html", job=job)


@main.route('/')
def home():
    # If logged in, go to dashboard, else go to login page
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))
