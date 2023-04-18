from .models import User, Course, User_Courses, db

# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy.orm import load_only

courses_web = Blueprint('courses_web',__name__)

# IP address of APP change as needed
BASE = "192.168.1.221:8000"


@courses_web.route('/Course')
@login_required
def course_web():

    
    #get info from html form: CHANGE
    # course_names = request.form.get('course_names')
    # semesters_ = request.form.get('semester')
    # availability_ = request.form.get('availability')

    if request.method == "POST":
        req = '/api/Course'

        # response = requests.post(BASE+req, json={
        #             "course_names": request.form.get('course_names'),
        #             "semester": r equest.form.get('semester'),
        #             "availability": request.form.get('availability'),
        #             })
    

# @courses.route('/api/findclassmates',methods=['GET'])
# @login_required
# def find_classmates():
#     return 
