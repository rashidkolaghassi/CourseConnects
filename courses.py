from .models import User, Course, User_Courses, db

# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy.orm import load_only

courses = Blueprint('courses',__name__)

@courses.route('/api/Course',methods=['GET','POST','DELETE'])
@login_required
def course():
    '''
    input format:
    '''
    if request.method == 'POST':

        course_names= request.json.get('course_names')
        semesters_ = request.json.get('semester')
        availability_ = request.json.get('availability')

        if len(semesters_)!=len(course_names):
            return jsonify({'ERROR':'courses and semesters dont line up'})
        for e in range(len(course_names)):
            #check if course is already in courses table:
            courseCheck = Course.query.filter_by(course_name=course_names[e],semester=semesters_[e]).first()
            if courseCheck is None:
                course_=Course(course_name=course_names[e],semester=semesters_[e])
                db.session.add(course_)
                db.session.commit()
                courseCheck = Course.query.filter_by(course_name=course_names[e],semester=semesters_[e]).first()

            
            course_=User_Courses(user_id=current_user.id,course_id=courseCheck.course_id, availability = availability_[e] )
            db.session.add(course_)
            db.session.commit()
        
        return jsonify({'message':'Sucessfully added courses'})

    elif request.method == 'GET':
        courses = Course.query.join(User_Courses).filter_by(user_id=current_user.id).all()
    
        return jsonify({'courses': [{'id': course.course_name, 'semester': course.semester} for course in courses]})
        
    elif request.method == 'DELETE':
        course_names= request.json.get('course_names')
        semesters_ = request.json.get('semester')
        if len(semesters_)!=len(course_names):
            return jsonify({'ERROR':'courses and semesters dont line up'})
        
        for e in range(len(course_names)):

            course_= User_Courses.query.filter_by(user_id=current_user.id).join(Course).filter_by(course_name=course_names[e],semester = semesters_[e]).first()
            
            if course_ is not None:
                db.session.delete(course_)
                db.session.commit()
            else:
                return {"message":"invalid course name entered"}
            
        return {"message":"successfuly deleted course"}
    

@courses.route('/api/findclassmates',methods=['GET'])
@login_required
def find_classmates():
    course_names= request.json.get('course_name')
    semester_=request.json.get('semesters')
    classmates_={}
    for e in range(len(course_names)):
        course= Course.query.filter_by(course_name=course_names[e],semester=semester_[e]).first()
        course_id=course.course_id
        users= User.query.join(User_Courses).filter(User_Courses.course_id == course_id, User.id != current_user.id).with_entities(User.first_name, User.last_name,User_Courses.availability).all()
        classmates_[course_names[e]]=[f'{user.first_name} {user.last_name} {user.availability}' for user in users]

    return jsonify(classmates_)
    

# @courses.route('/api/addfriends',methods=['GET'])
# @login_required
# def addfriends():






                
          
    

