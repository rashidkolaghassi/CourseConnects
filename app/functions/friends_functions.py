from ..models import User, Course, User_Courses, db, Friends
from flask_login import current_user
from flask import jsonify
from sqlalchemy import and_


def findClassmates(course_names, semester_):
    classmates_={}
    course= Course.query.filter_by(course_name=course_names,semester=semester_).first()
    if course is None:
         return {'message':'Course Doesnt Exist',
            'status':'400'}

    course_id=course.course_id
    #users= User.query.join(User_Courses).filter(User_Courses.course_id == course_id, User.id != current_user.id,User_Courses.status != -1).with_entities(User.first_name, User.last_name,User.username,User.email,User_Courses.status).all()

    users = User.query.join(User_Courses).filter(and_(
            User_Courses.course_id == course_id,
            User.id != current_user.id,
            User_Courses.status >= 0
        )).with_entities(User.first_name, User.last_name, User.username, User.email, User_Courses.status,User.id).all()

    classmates_['users'] = []
    for user in users:
        print(user.id)
        friend = Friends.query.filter_by(user_id=current_user.id, friend_id=user.id).first()
        if user.status == 1:
            classmates_['users'].append({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'friend': 1 if friend is not None else 0
            })
        elif user.status == 0:
            friend = Friends.query.filter_by(user_id=current_user.id, friend_id=user.id).first()
            if friend is not None:
                classmates_['users'].append({
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email,
                    'friend': 1
                })

    return classmates_


def addFriend(username):
    friendID = User.query.filter_by(username=username).first()
    if friendID is None:
        return({'message':'Error, username is not valid',
                    'status':'400'})

    friend = User.query.join(Friends, User.id == Friends.friend_id).filter(Friends.user_id == current_user.id, User.username == username).first()
    if friend:
        return({'message':'Error, username is already a friend',
                'status':'400'})
    
    friendship = Friends(user_id = current_user.id, friend_id=friendID.id)
    friendship_other = Friends(user_id = friendID.id, friend_id=current_user.id)
    db.session.add(friendship)
    db.session.add(friendship_other)
    db.session.commit()
    
    return {'message':'Successfully added friend',
            'status':'200'}



def getFriends():
    friends = User.query.join(Friends, User.id == Friends.friend_id).filter(Friends.user_id == current_user.id).all()
    return jsonify({'friends': [{'username': friend.username, 'first_name': friend.first_name, 'last_name':friend.last_name, 'email':friend.email} for friend in friends]})

def deleteFriend(username):
    friendID = User.query.filter_by(username=username).first()
    friend = User.query.join(Friends, User.id == Friends.friend_id).filter(Friends.user_id == current_user.id, User.username == username).first()
    if friend is None:
        return jsonify({'Message': 'Error, Friend Not Found',
               'status': '400'})
    else:
        print(friendID.id)
        friendship = Friends.query.filter_by(user_id=current_user.id,friend_id=friendID.id).first()
        db.session.delete(friendship)
        db.session.commit()

        return jsonify({"message":"successfuly deleted friendship",
                            'status':'200'})
