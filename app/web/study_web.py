from ..models import User, Course, User_Courses, db,Study,Study_Participants
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, url_for,Blueprint,jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required 
import requests 
from ..forms import  FindFriendsForm,AddStudyForm

import datetime


study_web = Blueprint('study_web',__name__)


from ..functions.courses_functions import addCourses, getCourses, deleteCourses
from ..functions.study_functions import find_study_sessions, create_study_session,join_study_session, my_study_sessions
msg=None
@study_web.route('/studysessions',methods=['GET','POST'])
@login_required
def studysession_web():
    global msg
    
    if request.method== 'GET':
        course_form = FindFriendsForm(request.form)
        local_msg=msg
        msg=None
        return render_template("study/home.html",form=course_form,userid=current_user.id,msg=local_msg)
        # return render_template("study/home.html",form=course_form,msg=local_msg)

    if request.method == 'POST':
        find_friends_form = FindFriendsForm(request.form)
        if 'find' in request.form:
            course_names = request.form.get('course_name')
            semesters_ = request.form.get('semester')

            response=find_study_sessions(course_names,semesters_).json
            print(response)
            return render_template("study/home.html",form=find_friends_form,study_sessions=response,userid=current_user.id)
        
@study_web.route('/joinsession',methods=['POST'])
@login_required
def joinsession_web():
     global msg
     if 'join' in request.form:
        study_id=request.form.get('study_id')
        response=join_study_session(study_id)
        msg=response['message']
        return redirect(url_for('study_web.studysession_web'))



@study_web.route('/mysessions',methods=['GET'])
@login_required
def mysessions_web():
    sessions = my_study_sessions().json
    return render_template("study/mysessions.html",sessions=sessions)




@study_web.route('/createsession',methods=['GET','POST'])
@login_required
def createsession_web():

    add_study_form = AddStudyForm(request.form)

    if request.method == 'GET':
        return render_template("study/createsession.html", form = add_study_form)

    if request.method == "POST":
            if 'add' in request.form:

                course_name = request.form.get('course_name')
                semester = request.form.get('semester')
                date=request.form.get('date')
                start_time=request.form.get('start_time')
                end_time=request.form.get('end_time')
                location=request.form.get('location')
                description=request.form.get('description')

                date=datetime.datetime.strptime(date,'%Y-%m-%d').date()
                start_time=datetime.datetime.strptime(start_time,'%H:%M').time()
                end_time=datetime.datetime.strptime(end_time,'%H:%M').time()

                response=create_study_session(course_name=course_name,semester=semester,date=date,start_time=start_time,end_time=end_time,location=location,description=description)


                if response.json['status'] == '200':
                    return render_template('study/createsession.html',msg='Successfully Created Study Session',form=add_study_form)


    