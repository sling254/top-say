from flask import render_template, redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from .forms import UpdateProfile, CreateBlog 
from ..models import User, Blog
from ..import db, photos
import secrets
import os
from ..email import mail_message

@main.route('/')
def index():

    return render_template('index.html')




@main.route('/new_post', methods=['POST','GET'])
@login_required
def new_blog():
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,description = description, content=content,user_id=user_id)
        blog.save()
        return redirect(url_for('main.index'))
    return render_template('post.html', form = form)


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

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    user = User.query.filter_by(username = name).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('main.profile',name=user.username,))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('profile/update.html', user = user, form =form)
