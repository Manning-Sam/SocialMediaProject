from app import app
from flask import render_template
from flask_login import login_required

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')