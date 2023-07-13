from flask import request, render_template, redirect, url_for, flash
import requests
from . import auth
from app import db
from app.blueprints.auth.forms import LoginForm, SignupForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html',form = form)
    else:
        return render_template('login.html',form = form)
    
@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        user_data = {
            'first_name' : form.first_name.data,
            'last_name' : form.last_name.data,
            'user_name': form.user_name.data,
            'email' : form.email.data.lower(),
            'password' : form.password.data
        }

        stat_data = {
            'points' : 0,
            'assists': 0,
            'rebounds':0,
            'games_played': 0
        }

        achievement_data = {
            'triple_double': 'False',
            'sus': 'False',
            'snell': 'False'
        }

        new_user = User()
        
        
        new_user.from_dict(user_data)
        new_user.from_stats(stat_data)
        new_user.from_achieve(achievement_data)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))