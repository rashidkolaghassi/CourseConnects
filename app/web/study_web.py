from ..models import User, Course, User_Courses, db,Study,Study_Participants
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, url_for,Blueprint,jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required 
import requests 
from ..forms import  FindFriendsForm


study_web = Blueprint('study_web',__name__)


from ..functions.courses_functions import addCourses, getCourses, deleteCourses
from ..functions.study_functions import find_study_sessions, create_study_session,join_study_session

@study_web.route('/studysessions',methods=['GET','POST'])
@login_required
def studysession_web():
    # global msg
    if request.method== 'GET':
        course_form = FindFriendsForm(request.form)
        # local_msg=msg
        # msg=None
        return render_template("study/home.html",form=course_form)
        # return render_template("study/home.html",form=course_form,msg=local_msg)

    if request.method == 'POST':
        find_friends_form = FindFriendsForm(request.form)
        if 'find' in request.form:
            course_names = request.form.get('course_name')
            semesters_ = request.form.get('semester')

            response=find_study_sessions(course_names,semesters_).json
            print(response)
            return render_template("study/home.html",form=find_friends_form,study_sessions=response)
