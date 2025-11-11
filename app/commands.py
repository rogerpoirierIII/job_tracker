from flask import current_app
from app import db
from app.models import User, Job
from werkzeug.security import generate_password_hash


def register_commands(app):
    @app.cli.command("seed_demo")
    def seed_demo():
        """Seed the database with a demo user and diverse sample job applications."""
        with app.app_context():
            print("🌱 Starting demo data seeding...")

            # Check if demo user exists
            demo_user = User.query.filter_by(email="demo@jobtracker.com").first()

            if not demo_user:
                demo_user = User(
                    username="demouser",
                    email="demo@jobtracker.com",
                    password_hash=generate_password_hash("password123")
                )
                db.session.add(demo_user)
                db.session.commit()
                print("Created demo user (demo@example.com / demo123)")
            else:
                print("Demo user already exists.")

            # Diverse demo job applications
            demo_jobs = [
                {
                    "title": "Software Engineer",
                    "company": "Google",
                    "status": "Interviewing",
                    "notes": "Completed phone screen. Next: onsite interviews next week.",
                    "website": "https://careers.google.com/",
                    "location": "Mountain View, CA",
                    "contact": "recruiter@google.com",
                    "salary": "$135,000"
                },
                {
                    "title": "Backend Developer",
                    "company": "Stripe",
                    "status": "Applied",
                    "notes": "Submitted application via company portal on Nov 1.",
                    "website": "https://stripe.com/jobs",
                    "location": "Remote (US)",
                    "contact": "careers@stripe.com",
                    "salary": "$125,000"
                },
                {
                    "title": "Data Analyst",
                    "company": "UnitedHealth Group",
                    "status": "Offer Received",
                    "notes": "Offer accepted. Start date in December pending paperwork.",
                    "website": "https://careers.unitedhealthgroup.com/",
                    "location": "Minneapolis, MN",
                    "contact": "hr@uhg.com",
                    "salary": "$95,000"
                },
                {
                    "title": "Frontend Engineer",
                    "company": "Figma",
                    "status": "Interview Scheduled",
                    "notes": "Interview scheduled for next Monday with design lead.",
                    "website": "https://www.figma.com/careers/",
                    "location": "Remote",
                    "contact": "recruiting@figma.com",
                    "salary": "$110,000"
                },
                {
                    "title": "DevOps Engineer",
                    "company": "Amazon Web Services",
                    "status": "Applied",
                    "notes": "Submitted through internal referral program.",
                    "website": "https://aws.amazon.com/careers/",
                    "location": "Seattle, WA",
                    "contact": "aws-recruit@amazon.com",
                    "salary": "$140,000"
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "OpenAI",
                    "status": "Researching",
                    "notes": "Reading about current projects before applying.",
                    "website": "https://openai.com/careers",
                    "location": "San Francisco, CA",
                    "contact": "careers@openai.com",
                    "salary": "$160,000"
                },
                {
                    "title": "Product Manager",
                    "company": "Spotify",
                    "status": "Applied",
                    "notes": "Applied via LinkedIn. Strong alignment with my background.",
                    "website": "https://www.spotifyjobs.com/",
                    "location": "New York, NY",
                    "contact": "pm-recruiter@spotify.com",
                    "salary": "$120,000"
                },
                {
                    "title": "Quality Assurance Engineer",
                    "company": "Adobe",
                    "status": "Interviewing",
                    "notes": "Passed technical test. Panel interview next week.",
                    "website": "https://adobe.wd5.myworkdayjobs.com/",
                    "location": "San Jose, CA",
                    "contact": "qa@adobe.com",
                    "salary": "$100,000"
                },
                {
                    "title": "Full Stack Developer",
                    "company": "Notion Labs",
                    "status": "Coding Challenge",
                    "notes": "Submitted take-home assignment. Awaiting feedback.",
                    "website": "https://www.notion.so/careers",
                    "location": "Remote",
                    "contact": "engineering@notion.so",
                    "salary": "$115,000"
                },
                {
                    "title": "Business Intelligence Analyst",
                    "company": "Meta",
                    "status": "Applied",
                    "notes": "Applied via internal referral. Recruiter said review in progress.",
                    "website": "https://www.metacareers.com/",
                    "location": "Menlo Park, CA",
                    "contact": "bi-team@meta.com",
                    "salary": "$110,000"
                },
                {
                    "title": "Cybersecurity Specialist",
                    "company": "CrowdStrike",
                    "status": "Rejected",
                    "notes": "Rejection received after technical interview.",
                    "website": "https://www.crowdstrike.com/careers/",
                    "location": "Austin, TX",
                    "contact": "security@crowdstrike.com",
                    "salary": "$125,000"
                },
                {
                    "title": "Technical Writer",
                    "company": "Atlassian",
                    "status": "Offer Declined",
                    "notes": "Declined offer due to compensation mismatch.",
                    "website": "https://www.atlassian.com/company/careers",
                    "location": "Remote",
                    "contact": "recruiting@atlassian.com",
                    "salary": "$90,000"
                }
            ]

            # Add jobs if not already in DB
            for job_data in demo_jobs:
                existing_job = Job.query.filter_by(
                    title=job_data["title"],
                    company=job_data["company"],
                    user_id=demo_user.id
                ).first()

                if not existing_job:
                    new_job = Job(user_id=demo_user.id, **job_data)
                    db.session.add(new_job)

            db.session.commit()
            print("Demo data seeded")
