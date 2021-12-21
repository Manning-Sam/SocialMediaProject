from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash


from .forms import LoginForm, UserInfoForm
from app.models import User

from app.models import db


from flask_login import login_user, logout_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/login', methods=['GET',"POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        print("validate")
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

     
        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            return redirect(url_for('auth.logMeIn'))
        
      
        login_user(user, remember = remember_me)
        return redirect(url_for('blog.blogHome'))
    return render_template('login.html', form = form)

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    my_form = UserInfoForm()
    if request.method == "POST":
        print("post method requested")
        if my_form.validate():
            print("form validated")
            
            username = my_form.username.data
            email = my_form.email.data
            password = my_form.password.data

           
            user = User(username, email, password)
            print("user instanciated")
            
            db.session.add(user)
           
            db.session.commit()
            print("commited to database")

            return redirect(url_for('home'))


        else:
            print('Not validated! :(')
    return render_template('signup.html', form = my_form )

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))