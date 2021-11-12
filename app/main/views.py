from flask import render_template, redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User
from ..import db, photos
import secrets
import os
from ..email import mail_message

@main.route('/')
def index():

    return render_template('index.html')


@main.route('/profile/<name>',methods = ['POST','GET'])
@login_required
def profile(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return render_template('profile/profile.html',user = user)