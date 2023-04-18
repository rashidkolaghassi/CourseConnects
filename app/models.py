from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email=db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    user_courses = db.relationship('User_Courses')
    # friends= db.relationship('Friends')

    
class Course(db.Model):
    course_id = db.Column(db.Integer,primary_key=True)
    course_name=db.Column(db.String(50))
    semester = db.Column(db.String(50)) 
    user_courses=db.relationship('User_Courses')

class User_Courses(db.Model):
     
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     course_id=db.Column(db.Integer,db.ForeignKey('course.course_id'))
     # availability takes -1 for unavailable, 0 for friends only, 1 for everyone
     availability = db.Column(db.Integer)

     __table_args__ = (
    db.PrimaryKeyConstraint(
        user_id, course_id,
        ),
    )


class Friends(db.Model):
    friendship_id=db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
    friend_id= db.Column(db.Integer,db.ForeignKey('user.id'))


