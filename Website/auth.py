from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Password incorrect', category='error')
        else:
            flash('Email does not exist', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already in use', category='error')
        elif firstName == 'Voldemort':
            flash('You musn\'t say his name',  category='error')
        elif password1 != password2:
            flash('Passwords are not equal!', category='error')
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='sha256')) 
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Sign up successful!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)


@auth.route('/share', methods=['GET', 'POST'])
@login_required
def see_gifts():
    if request.method == 'POST':
        user = current_user
        user.access_phrase = request.form.get('access_phrase')
        db.session.commit()
        flash('Access phrase successfully updated!')
    return render_template("share.html", user=current_user)

@auth.route('/view', methods=['GET', 'POST'])
@login_required
def view_gifts():
    gifts = None
    name = None
    viewing = False
    if request.method == 'POST':
        fr_phr = request.form.get('friend_ap')
        fr_email = request.form.get('friend_email')
        friend = User.query.filter_by(email=fr_email).first_or_404('Email id not found in database. Please go back and try again.')
        if friend.access_phrase == fr_phr:
            gifts = friend.gifts
            name = friend.first_name
            viewing = True
        else:
            flash('Incorrect access phrase', category='error')
    return render_template("view.html", user = current_user, name = name, gifts = gifts, viewing = viewing)
