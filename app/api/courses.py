from ..models import User, Course, User_Courses, db
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy.orm import load_only
import requests

from ..functions.courses_functions import addCourses, getCourses, deleteCourses


# IP address of APP change as needed
BASE = "http://192.168.1.6:8000/"



courses = Blueprint('courses',__name__)

@courses.route('/api/Course',methods=['GET','POST','DELETE'])
@login_required
def course():
    '''
    input format:
    '''
    if request.method == 'POST':

        course_names= request.json.get('course_names')
        semesters_ = request.json.get('semesters')
        status_ = request.json.get('status')

        response = addCourses(course_names,semesters_,status_)

        return response
        

    elif request.method == 'GET':
        return getCourses()
        
    elif request.method == 'DELETE':
        course_names= request.json.get('course_names')
        semesters_ = request.json.get('semesters')
        return deleteCourses(course_names, semesters_)
      
    

@courses.route('/api/findclassmates',methods=['GET'])
@login_required
def find_classmates():
    course_names= request.json.get('course_name')
    semester_=request.json.get('semesters')
    classmates_={}
    for e in range(len(course_names)):
        course= Course.query.filter_by(course_name=course_names[e],semester=semester_[e]).first()
        course_id=course.course_id
        users= User.query.join(User_Courses).filter(User_Courses.course_id == course_id, User.id != current_user.id).with_entities(User.first_name, User.last_name,User_Courses.status).all()
        classmates_[course_names[e]]=[f'{user.first_name} {user.last_name} {user.status}' for user in users]

    return jsonify(classmates_)
    

# @courses.route('/api/addfriends',methods=['GET'])
# @login_required
# def addfriends():


