from ..models import User, Course, User_Courses, db, Study,Friends,Study_Participants
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy.orm import load_only
from datetime import date
from datetime import time
import datetime


import requests

from ..functions.courses_functions import addCourses, getCourses, deleteCourses
from ..functions.friends_functions import findClassmates,addFriend, getFriends
from ..functions.study_functions import find_study_sessions,create_study_session,delete_study_session,join_study_session,my_study_sessions

study = Blueprint('StudySessions',__name__)

@login_required
@study.route('/api/studysessions',methods=['GET','POST'])
def studysession():
    if request.method=='GET':
        course_name=request.json.get('course_name')
        semester=request.json.get('semester')

        response=find_study_sessions(course_name,semester)
        return response
    
    if request.method=='POST':
        course_name=request.json.get('course_name')
        semester=request.json.get('semester')
        date=request.json.get('date')
        start_time=request.json.get('start_time')
        end_time=request.json.get('end_time')
        location=request.json.get('location')
        description=request.json.get('description')

        date=datetime.datetime.strptime(date,'%m/%d/%Y').date()
        start_time=datetime.datetime.strptime(start_time,'%I:%M %p').time()
        end_time=datetime.datetime.strptime(end_time,'%I:%M %p').time()


        response=create_study_session(course_name=course_name,semester=semester,date=date,start_time=start_time,end_time=end_time,location=location,description=description)
        return response 






@login_required
@study.route('/api/joinstudysession',methods=['POST'])
def joinstudysession():

    if request.method=='POST':
        study_id=request.json.get('study_id')

        response=join_study_session(study_id)
        return jsonify(response)
    
@login_required
@study.route('/api/mysessions',methods=['GET'])
def mystudysession():
    response=my_study_sessions()
    return response
