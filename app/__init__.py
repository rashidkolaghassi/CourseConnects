from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import os


db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SECRET_KEY'] = 'your_secret_key'

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
        'app_name': "CourseConnects"
    }
)
    
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
    from .api.study_sessions import study
    from .web.study_web import study_web
    
    
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(courses,url_prefix='/')
    app.register_blueprint(courses_web,url_prefix='/')
    app.register_blueprint(misc_web,url_prefix='/')
    app.register_blueprint(Friends_web,url_prefix='/')
    app.register_blueprint(friends, url_prefix='/')
    app.register_blueprint(study,url_prefix='/')
    app.register_blueprint(study_web,url_prefix='/')
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    
    @login_manager.user_loader
    def user_loader(user_id): 
        return User.query.get(user_id)
  
    return app

   