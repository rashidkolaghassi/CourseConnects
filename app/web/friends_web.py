from ..models import User, Course, User_Courses, db
from ..forms import AddCoursesForm, FindFriendsForm

# Third-party libraries
from flask import Flask, redirect, url_for,Blueprint,jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required 
import requests 


Friends_web = Blueprint('friends_web',__name__)

# IP address of APP change as needed
BASE = "http://192.168.1.6:8000/"
#from .auth import sesh
msg=None
from ..functions.courses_functions import addCourses, getCourses, deleteCourses
from ..functions.friends_functions import findClassmates,addFriend, getFriends, deleteFriend

@Friends_web.route('/Friends',methods=['GET','POST'])
@login_required
def friends_web():
    global msg
    if request.method== 'GET':
        find_friends_form = FindFriendsForm(request.form)
        local_msg=msg
        msg=None
       
        return render_template("friends/home.html",form=find_friends_form,msg=local_msg)

    if request.method == 'POST':
        find_friends_form = FindFriendsForm(request.form)
        if 'find' in request.form:
            course_names = request.form.get('course_name')
            semesters_ = request.form.get('semester')

            response=findClassmates(course_names,semesters_)
            print(response)
            return render_template("friends/home.html",form=find_friends_form,friends=response)

            

@Friends_web.route('/addfriend',methods=['GET','POST'])
@login_required
def addFriends():
    global msg
    if 'add' in request.form:
        username=request.form.get('username')
        response=addFriend(username)
        msg=response['message']
        return redirect(url_for('friends_web.friends_web'))
    

@Friends_web.route('/myFriends',methods=['GET','POST'])
@login_required
def getmyFriends():
    if request.method == "GET":
        friends=getFriends().json
        return render_template("friends/myfriends.html",friends=friends)
    
    if request.method =="POST":
       
        username = request.form.get("username")
        response = deleteFriend(username).json
        friends=getFriends().json
        return render_template("friends/myfriends.html",friends=friends,msg=response['message'])


        

    
        



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
