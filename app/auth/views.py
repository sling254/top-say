from flask import render_template,url_for,flash,redirect,request
from . import auth
from flask_login import login_user,login_required,logout_user
from .forms import RegForm,LoginForm
from ..models import User
from .. import db
from ..email import mail_message



@auth.route('/login', methods = ['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user != None and user.verify_password(form.password.data):
      login_user(user,form.remember_me.data)
      return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or Password')
  return render_template('auth/login.html', form = form)


