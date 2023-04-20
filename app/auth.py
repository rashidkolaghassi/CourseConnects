# Third-party libraries
from flask import Flask, redirect, request, url_for,Blueprint,jsonify,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
import requests
from .forms import LoginForm, CreateAccountForm
import json

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Internal imports
from .models import User, Course, db
#sesh = requests.Session()

auth = Blueprint('auth',__name__)
BASE = "http://192.168.1.6:8000"


@auth.route('/', methods=['GET'])
def home():
    print(current_user.is_authenticated)
    if current_user.is_authenticated == True:
        return render_template("home/index.html")
    else:
        return redirect(url_for('auth.login_web'))


@auth.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name=request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already taken.'}), 400
    user = User(username=username, password=password,first_name=first_name,last_name=last_name, email = email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created.'})


@auth.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user,remember=True)
        print(current_user.id)
        print(f'authent: {current_user.is_authenticated}')
        return jsonify({'message': f'Logged in as {username}.',
                        'status':'200'})
    else:
        return jsonify({'message': 'Invalid credentials.',
                        'status':'400'})


@auth.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out.'})


## web app logins 
@auth.route('/register', methods=['GET','POST'])
def register_web():

    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        first_name= request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password=request.form['password']

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = User(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@auth.route('/login', methods=['GET','POST'])
def login_web():
    login_form=LoginForm(request.form)
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user,remember=True)
                # create API sesh and authenticate it for future calls
                
                # sesh.post(BASE+"/api/login",json={"username":username,
                #                 "password":password
                #                 })
    
            return redirect(url_for('auth.home'))
        else:
            return render_template("accounts/login.html",form=login_form)

            #     payload = json.dumps({"username":request.form.get('username'),
            #                            "password":request.form.get('password')
            #                 })

            #     headers = {
            #     'Content-Type': 'application/json',
            #     'Cookie': 'remember_token=1|8b3414488f03cf6251b8317c8d22ed254da149b528bf0590c03a2779339bd2734d4e7a862a5fe0b9af12804705df31c9c9fb91bcb863001db4eae7eaa49e082b; session=.eJwlzjsOwjAMANC7ZGaIHSd2epnKvwjWlk6Iu1OJCzy9T9nXkeezbO_jykfZX1G20iR4SAoQGyd2DxcIJuMGQjTdQgMIw9mwtorcjWkZZfXJHaBOBl8U2LrqItDZSSuHtMiRIeHYpJI2tUq8SMct4lg5QdG03JHrzOO_gfL9AaQGL4M.ZD7HOw.uY3KIOjeax4NmcRbG6OAefihIRc'
            #     }

            #     response=requests.post(BASE+"/api/login" , headers=headers, data= payload)
            #     print(response.json())
            # if response.json()["status"]=='200':
            # if response.json()["status"]=='200':
                # print(f'here: {current_user.id}')
                # print(f'authent: {current_user.is_authenticated}')
    return render_template("accounts/login.html",form=login_form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout_web():
    logout_user()
    return redirect(url_for('auth.home'))