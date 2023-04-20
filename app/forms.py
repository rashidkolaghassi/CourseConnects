# -*- encoding: utf-8 -*-
# credit to present AppSeed.us, code avaliblie at https://github.com/app-generator/flask-pixel
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    first_name = StringField('First Name',
                         id='first_name',
                         validators=[DataRequired()])
    last_name = StringField('Last Name',
                         id='lastname_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])


class AddCoursesForm(FlaskForm):
    course_name = StringField('Course Name',
                         id='coursename_create',
                         validators=[DataRequired()])
    semester = StringField('Semester',
                         id='semester_create',
                         validators=[DataRequired()])
    status = SelectField('Status',
                         choices=[-1,0,1],
                         id='status_create',
                         validators=[DataRequired()],
                         coerce=str)
    # status = StringField('Status',
    #                      id='status_create',
    #                      validators=[DataRequired()])
