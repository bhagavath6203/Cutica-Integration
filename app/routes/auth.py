# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from app.services.gmail_service import send_email
from pymongo.errors import ServerSelectionTimeoutError
from bson.objectid import ObjectId
import secrets
# from flask_pymongo import PyMongo

from app.routes import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('loginEmail')
            password = request.form.get('loginPassword')
            user = mongo.db.users.find_one({'email': email})
            if user and user['password'] == password:  # Note: Consider using password hashing
                session['username'] = user['username']
                session['email'] = email
                session['role'] = user.get('role', 'user')
                flash('Login successful!', 'success')
                if session['role'] == 'admin':
                    return redirect(url_for('auth.dashboard_page'))
                else:
                    return redirect(url_for('auth.home', username=user['username']))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        except ServerSelectionTimeoutError:
            flash('Could not connect to database. Please try again later.', 'danger')
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get('signUpUsername')
            email = request.form.get('signUpEmail')
            password = request.form.get('signUpPassword')
            
            if mongo.db.users.find_one({'email': email}):
                flash('Email already exists', 'danger')
                return redirect(url_for('auth.signup'))
            else:
                mongo.db.users.insert_one({
                    'username': username, 
                    'email': email, 
                    'password': password,  # Note: Consider using password hashing
                    'role': 'admin'  # Note: Consider if all new users should be admins
                })
                flash('Sign up successful!', 'success')
                return redirect(url_for('auth.login'))
        except ServerSelectionTimeoutError:
            flash('Could not connect to MongoDB. Please try again later.', 'danger')
    return render_template('signup.html')

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        try:
            email = request.form.get('forgotPasswordEmail')
            user = mongo.db.users.find_one({'email': email})
            if user:
                token = secrets.token_urlsafe(32)
                mongo.db.password_resets.insert_one({'email': email, 'token': token})
                reset_url = url_for('auth.reset_password', token=token, _external=True)
                subject = 'Password Reset Request'
                body = f'Click the link to reset your password: {reset_url}'
                send_email(email, subject, body)
                flash('A password reset link has been sent to your email.', 'info')
            else:
                flash('Email not found', 'danger')
        except ServerSelectionTimeoutError:
            flash('Could not connect to MongoDB. Please try again later.', 'danger')
    return render_template('forgot_password.html')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = mongo.db.password_resets.find_one({'token': token})
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        new_password = request.form.get('newPassword')
        mongo.db.users.update_one({'email': user['email']}, {'$set': {'password': new_password}})
        mongo.db.password_resets.delete_one({'token': token})
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)

@bp.route('/home/<username>')
def home(username):
    return render_template('home.html', username=username)
@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))