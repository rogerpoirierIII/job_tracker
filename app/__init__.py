from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view =  'main.login' #Redirects page to login page is authentications fails

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # This function reloads the user object from the user ID stored in session
    return User.query.get(int(user_id))
