from flask import current_app
from app import db
from app.models import User, Job
from werkzeug.security import generate_password_hash

def register_commands(app):
    @app.cli.command("seed_demo")
    def seed_demo():
        """Seed the database with a demo user and sample job applications."""
        with app.app_context():
            demo_user = User.query.filter_by(email="demo@jobtracker.com").first()
            if demo_user:
                print("Demo user already exists — skipping.")
                return

            demo_user = User(
                username="demouser",
                email="demo@jobtracker.com",
                password_hash=generate_password_hash("password123")
            )
            db.session.add(demo_user)
            db.session.commit()

            demo_jobs = [
                Job(
                    title="Software Engineer",
                    company="Google",
                    status="Interviewing",
                    notes="Completed initial phone screen. Waiting for next round.",
                    user_id=demo_user.id,
                    website="https://careers.google.com/",
                    location="Mountain View, CA",
                    contact="recruiter@google.com",
                    salary="$130,000"
                ),
                Job(
                    title="Backend Developer",
                    company="Stripe",
                    status="Applied",
                    notes="Application submitted on 10/15. Referred by current employee.",
                    user_id=demo_user.id,
                    website="https://stripe.com/jobs",
                    location="Remote (US)",
                    contact="careers@stripe.com",
                    salary="$125,000"
                ),
                Job(
                    title="Data Analyst",
                    company="UnitedHealth Group",
                    status="Offer Received",
                    notes="Offer accepted. Start date pending background check.",
                    user_id=demo_user.id,
                    website="https://careers.unitedhealthgroup.com/",
                    location="Minneapolis, MN",
                    contact="hr@uhg.com",
                    salary="$95,000"
                ),
                Job(
                    title="Frontend Engineer",
                    company="Figma",
                    status="Interview Scheduled",
                    notes="First interview scheduled for next Monday via Zoom.",
                    user_id=demo_user.id,
                    website="https://www.figma.com/careers/",
                    location="Remote",
                    contact="recruiting@figma.com",
                    salary="$110,000"
                )
            ]

            db.session.add_all(demo_jobs)
            db.session.commit()

            print("✅ Demo user and sample job applications added successfully!")
