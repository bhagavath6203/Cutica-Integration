from app.routes import bp
from flask import render_template, session, redirect, url_for, request, flash, current_app
# from app.services import send_email
from app import mongo
from app.services.gmail_service import send_email
import secrets
@bp.route('/support_team')
def support_team():
    admin_email = session.get('email')
    support_members = mongo.db.support_team.find({'admin_email': admin_email})
    return render_template('support_team.html', support_members=support_members)

@bp.route('/add_support')
def add_support():
    return render_template('add_support.html')

#Add support credentials POST request route: Handle adding new support credentials
@bp.route('/new_support_credentials', methods=['POST'])
def new_support_credentials():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    admin_email = session.get('email')

    # Generate random password and support ID
    password = secrets.token_urlsafe(12)
    support_id = secrets.randbelow(1000)  # Generate a random support ID (0-999)

    # Insert support member into users collection
    mongo.db.users.insert_one({'username': name, 'email': email, 'password': password, 'role': 'support'})

    # Insert support member details into support_team collection
    mongo.db.support_team.insert_one({'support_id': support_id, 'name': name, 'email': email, 'phone': phone, 'admin_email': admin_email})

    # Send email with credentials
    subject = 'Your Support Account Credentials'
    body = f'Username: {email}\nPassword: {password}\nSupport ID: {support_id}'
    send_email(current_app.gmail_service, email, subject, body)

    flash('Support member added and credentials sent!', 'success')
    return redirect(url_for('auth.support_team'))
