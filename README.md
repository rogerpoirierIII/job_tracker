# Job Tracker Web Application

A full-stack Flask web application that helps job seekers track applications, monitor progress, and stay organized throughout their job search.  
Built to showcase end-to-end software engineering skills including database design, authentication, CRUD functionality, and cloud deployment.

---

## Live Demo

**Deployed on Render:** [Application Tracker](https://job-tracker-idyl.onrender.com/) 




---

## Features

- **User Authentication**  
  Secure sign-up, login, and logout using Flask-Login and password hashing.

- **Job Application Management**  
  Create, view, update, and delete job applications. Track company name, role, status, application date, notes, and more.

- **Progress Tracking**  
  Visual indicators show the stage of each application (Applied, Interviewing, Offer, etc.).

- **Responsive UI**  
  Mobile-friendly front end using Bootstrap for clean, professional styling.

- **Persistent Cloud Database**  
  PostgreSQL database hosted on Render with schema migrations managed by Flask-Migrate/Alembic.

---

## Tech Stack

- **Backend:** Python 3, Flask, SQLAlchemy, Flask-Login, Flask-Migrate  
- **Frontend:** HTML5, CSS3, Bootstrap  
- **Database:** PostgreSQL  
- **Deployment:** Render (Gunicorn WSGI server)  
- **Environment & Config:** `python-dotenv` for local development, environment variables for production


---

## ⚙️ Local Development Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/job_tracker.git
   cd job_tracker
2. **Create local environment**
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate    # Windows
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Set environment variables**
   Create a .env file in project root
   ```env
   SECRET_KEY=your-secret-key
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=jobtracker_db
5. **Initialize and migrate the database**
   ```bash
   flask db upgrade
6. **Run the app**
   ```bash
   flask run
Visit http://127.0.0.1:5000 in your browser.
