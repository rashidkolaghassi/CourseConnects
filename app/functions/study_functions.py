from ..models import User, Course, User_Courses, db, Friends,Study_Sessions
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from flask import jsonify
from sqlalchemy import and_

def find_study_sessions(course_name,semester):
    course=Course.query.filter_by(course_name=course_name,semester=semester).first()
    if course is None:
                course_=Course(course_name=course_name,semester=semester)
                db.session.add(course_)
                db.session.commit()
                course = Course.query.filter_by(course_name=course_name,semester=semester).first()

    study_sessions=Study_Sessions.query.filter_by(course_id=course.course_id).all()
    return jsonify({'study_sessions': [{'id': study.course_id, 'owner': study.owner, 'course_name':course_name, 'semester': semester,'participants':study.participants} for study in study_sessions]})




def create_study_session(course_name,semester,date,time,location,description):
    course=Course.query.filter_by(course_name=course_name,semester=semester).first()
    if course is None:
                    course_=Course(course_name=course_name,semester=semester)
                    db.session.add(course_)
                    db.session.commit()
                    course = Course.query.filter_by(course_name=course_name,semester=semester).first()

    participant=str(current_user.id)+','
    study=Study_Sessions(course_id=course.course_id,owner=current_user.id,date=date,time=time,location=location,participants=participant,description=description)
    db.session.add(study)
    db.session.commit()
    return jsonify({'message':'Sucessfully created study Session',
                    'status':'200'})


def delete_study_session():
    return 
