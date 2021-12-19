from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash


from .forms import LoginForm, UserInfoForm
from app.models import User, Post


from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.models import db


@auth.route('/login', methods=['GET',"POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

     
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            return redirect(url_for('auth.logMeIn'))
        
      
        login_user(user, remember = remember_me)
        print(current_user)
        return redirect(url_for('home'))

    return render_template('login.html', form = form)

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    my_form = UserInfoForm()
    if request.method == "POST":
        if my_form.validate():
            
            username = my_form.username.data
            email = my_form.email.data
            password = my_form.password.data

           
            user = User(username, email, password)
            
            db.session.add(user)
           
            db.session.commit()

            return redirect(url_for('home'))


        else:
            print('Not validated! :(')
    return render_template('signup.html', form = my_form )

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))