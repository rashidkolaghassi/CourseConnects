from .models import User, Course, User_Courses, db
from flask_login import current_user
from flask import jsonify

def addCourses(course_names,semesters_,status_):
    if len(semesters_)!=len(course_names):
            return jsonify({'message':'ERROR, courses and semesters dont line up',
                            'status':'400'})
    for e in range(len(course_names)):
        #check if course is already in courses table:
        courseCheck = Course.query.filter_by(course_name=course_names[e],semester=semesters_[e]).first()
        if courseCheck is None:
            course_=Course(course_name=course_names[e],semester=semesters_[e])
            db.session.add(course_)
            db.session.commit()
            courseCheck = Course.query.filter_by(course_name=course_names[e],semester=semesters_[e]).first()

        
        course_=User_Courses(user_id=current_user.id,course_id=courseCheck.course_id, status = status_[e] )
        db.session.add(course_)
        db.session.commit()
        
    return jsonify({'message':'Sucessfully added courses',
                    'status':'200'})

def deleteCourses(course_names,semesters_):
        if len(semesters_)!=len(course_names):
            return jsonify({'message':'ERROR, courses and semesters dont line up',
                            'status':'400'})
        
        for e in range(len(course_names)):
            course_= User_Courses.query.filter_by(user_id=current_user.id).join(Course).filter_by(course_name=course_names[e],semester = semesters_[e]).first()
            if course_ is not None:
                db.session.delete(course_)
                db.session.commit()
            else:
                return jsonify({"message":"invalid course name entered",
                        "status": "400"})
      
        return jsonify({"message":"successfuly deleted course",
                        'status':'200'})

def getCourses():
    # courses = Course.query.join(User_Courses).filter_by(user_id=current_user.id).all()
    # courses = User_Courses.query.filter_by(user_id=current_user.id).join(Course).all()
    courses=Course.query.join(User_Courses).filter(User_Courses.user_id==current_user.id)\
        .add_columns(User_Courses.status,Course.course_name,Course.semester).all()
    return jsonify({'courses': [{'id': course.course_name, 'semester': course.semester, 'status':course.status} for course in courses]})

     