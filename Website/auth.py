
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Try again.', category='error')
        else:
            flash('That User does not exist', category='error')
    return render_template('login.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        imposter = User.query.filter_by(username=username).first()
        imposter2 = User.query.filter_by(email=email).first()
        if password == password2:
            if len(password) < 8:  #
                flash('Please, enter a longer password', category='error')
            if imposter2 :
                flash('Email already in use!', category='error')
            if imposter:
                flash('Username already in use!', category='error')
            elif len(email) <= 10:
                flash('Enter a valid Email address', category='error')
            elif len(username) < 3:
                flash('Username must be greater than 3 characters', category='error')
            else:
                new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256')) #Creating a new user
                db.session.add(new_user)  #Adding the new user to the database
                db.session.commit()  #Persisting the newly created items on the database
                login_user(new_user, remember=True)
                flash('Account successfully created', category='success')
                return redirect(url_for('views.home'))
            
        else:
            flash(request, 'Passwords do not match!')

    return render_template('signup.html', user = current_user)