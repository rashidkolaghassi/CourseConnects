from ..models import User, Course, User_Courses, db, Friends
from flask_login import current_user
from flask import jsonify

def getFriends():
    friends=User.query.join(Friends).filter_by(user_id=current_user.id)


def addFriend():
    return