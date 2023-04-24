from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from flask_httpauth import HTTPBasicAuth

db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    db.init_app(app)
    
    from .models import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)


    from .auth import auth
    from .api.courses import courses
    from .web.courses_web import courses_web
    from .web.misc_web import misc_web
    from .web.friends_web import Friends_web
    from .api.friends import friends
    
    
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(courses,url_prefix='/')
    app.register_blueprint(courses_web,url_prefix='/')
    app.register_blueprint(misc_web,url_prefix='/')
    app.register_blueprint(Friends_web,url_prefix='/')
    app.register_blueprint(friends, url_prefix='/')
    
    @login_manager.user_loader
    def user_loader(user_id): 
        return User.query.get(user_id)
  
    return app

   