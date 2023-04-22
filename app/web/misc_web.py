# Third-party libraries
from flask import Flask, redirect, url_for,Blueprint,render_template
from flask_login import UserMixin, current_user, login_required 


misc_web = Blueprint('misc_web',__name__)



@misc_web.route('/About',methods=['GET'])
@login_required
def about():
    return render_template("home/about.html")


@misc_web.route('/Contact',methods=['GET'])
@login_required
def contact():
    return render_template("home/contact.html")
        

