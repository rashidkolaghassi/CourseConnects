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
      
    




