
from ..models import User, Course, User_Courses, db
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy.orm import load_only
import requests

from ..functions.courses_functions import addCourses, getCourses, deleteCourses
from ..functions.friends_functions import findClassmates,addFriend, getFriends


friends = Blueprint('friends',__name__)

@friends.route('/api/findfriends',methods=['GET'])
@login_required
def find_classmates():
    course_name= request.json.get('course_name')
    semester_=request.json.get('semester')

    classmates_= findClassmates(course_name, semester_)

    return jsonify(classmates_)

@friends.route('/api/addfriend',methods=['POST'])
@login_required
def add_friend():
    username=request.json.get('username')
    response=addFriend(username)
    return response

@friends.route('/api/getfriends',methods=['GET'])
@login_required
def get_friend():
    response=getFriends()
    return response


    