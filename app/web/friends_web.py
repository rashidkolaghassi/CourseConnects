from ..models import User, Course, User_Courses, db
from ..forms import AddCoursesForm

# Third-party libraries
from flask import Flask, redirect, url_for,Blueprint,jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required 
import requests 


Friends_web = Blueprint('friends_web',__name__)
all_too=3

# IP address of APP change as needed
BASE = "http://192.168.1.6:8000/"
#from .auth import sesh

from ..functions.courses_functions import addCourses, getCourses, deleteCourses

@Friends_web.route('/Friends',methods=['GET'])
@login_required
def friends_web():
    if request.method == 'GET':
        courses=getCourses().json
        return render_template("friends/home.html",courses=courses)
        



# @courses_web.route('/FindFriends',methods=['GET','POST'])
# @login_required
# def addCourse():

#     add_courses_form = AddCoursesForm(request.form)

#     if request.method == 'GET':
#             return render_template("scheduling/addCourses.html", form = add_courses_form)

#     if request.method == "POST":
#             if 'add' in request.form:
    
#                 course_names = request.form.get('course_name')
#                 semesters_ = request.form.get('semester')
#                 status_ = request.form.get('status')

#                 response = addCourses([course_names],[semesters_],status_)

#                 if response.json['status'] == '200':
#                     return render_template('scheduling/addCourses.html',msg='Successfully Added Course',form=add_courses_form)
#                 else:
#                      return render_template('scheduling/addCourses.html',msg='Successfully Added Course',form=add_courses_form)
                     
#             else:
#                 return render_template("scheduling/addCourses.html", form = add_courses_form)



# @courses_web.route('/deleteCourse',methods=['GET','POST'])
# @login_required
# def deleteCourse():
#     delete_courses_form = AddCoursesForm(request.form)

#     if request.method == 'GET':
#             return render_template("scheduling/deleteCourses.html", form = delete_courses_form)

#     if request.method == "POST":
#             if 'delete' in request.form:
    
#                 course_names = request.form.get('course_name')
#                 semesters_ = request.form.get('semester')

#                 response = deleteCourses([course_names],[semesters_])
#                 print(response.json)

#                 if response.json['status'] == '200':
#                     return render_template('scheduling/deleteCourses.html',msg='Successfully Deleted Course',form=delete_courses_form)
#                 else:
#                     return render_template("scheduling/deleteCourses.html", msg='Error in inputted course info. Try again', form = delete_courses_form)
                 


# @courses_web.route('/Course',methods=['GET','POST','DELETE'])
# @login_required
# def course_rand():
#     return render_template("home/contact.html")

# @courses.route('/api/findclassmates',methods=['GET'])
# @login_required
# def find_classmates():
#     return 
