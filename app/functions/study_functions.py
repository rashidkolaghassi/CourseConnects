from ..models import User, Course, User_Courses, db, Friends,Study,Study_Participants
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from flask import jsonify
from sqlalchemy import and_
from datetime import time
from datetime import date

def find_study_sessions(course_name,semester):
    course=Course.query.filter_by(course_name=course_name,semester=semester).first()
    if course is None:
                course_=Course(course_name=course_name,semester=semester)
                db.session.add(course_)
                db.session.commit()
                course = Course.query.filter_by(course_name=course_name,semester=semester).first()

    study_sessions=Study.query.filter_by(course_id=course.course_id).all()
    
    return jsonify({'study_sessions': [{'study_id':study.study_id,'course_id': study.course_id,'date':study.date.strftime("%b %d %Y"), 'owner': study.owner,'start_time':study.start_time.strftime("%I:%M %p"),'end_time':study.end_time.strftime("%I:%M %p"), 'course_name':course_name, 'semester': semester,'participants':[participant.user_id for participant in study.participants]} for study in study_sessions]})


def create_study_session(course_name,semester,date,start_time,end_time,location,description):
    course=Course.query.filter_by(course_name=course_name,semester=semester).first()
    if course is None:
                    course_=Course(course_name=course_name,semester=semester)
                    db.session.add(course_)
                    db.session.commit()
                    course = Course.query.filter_by(course_name=course_name,semester=semester).first()
    
    study=Study(course_id=course.course_id,owner=current_user.id,date=date,start_time=start_time,end_time=end_time,location=location,description=description)
    
    db.session.add(study)
    db.session.commit()
    print(f'study_id = {study.study_id}')
    study_participant=Study_Participants(user_id=current_user.id,study_id=study.study_id)
    db.session.add(study_participant)
    db.session.commit()

    return jsonify({'message':'Sucessfully created study Session',
                    'status':'200'})




def join_study_session(study_id):
    study_check=Study_Participants.query.filter_by(user_id=current_user.id,study_id=study_id).first()

    if study_check:
            return jsonify({'message':'Error, already in study session',
                'status':'400'})
    
    else:

        study_participant=Study_Participants(user_id=current_user.id,study_id=study_id)
        db.session.add(study_participant)
        db.session.commit()
    
    return {'message':'Sucessfully joined study Session',
                    'status':'200'}



def my_study_sessions():
    sessions=Study.query.join(Study_Participants).\
            filter(Study_Participants.user_id == current_user.id).all()
    
    return jsonify ({'sessions': [{
                                   'course_name': Course.query.filter_by(course_id=session.course_id).first().course_name, 
                                   'semester': Course.query.filter_by(course_id=session.course_id).first().semester,
                                   'start_time':session.start_time.strftime('%I:%M %p'),
                                   'end_time': session.end_time.strftime('%I:%M %p'),
                                   'location':session.location,
                                   'description':session.description
                                   } for session in sessions]})

def delete_study_session():
    return 
