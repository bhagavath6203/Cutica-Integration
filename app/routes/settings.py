from app.routes import bp
from flask import render_template, redirect, url_for, session
from app import mongo

# Email configuration page route: Render email configuration page
@bp.route('/email_config')
def email_config():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('email_config.html')

# Classification configuration page route: Render classification configuration page
@bp.route('/classification_config')
def classification_config():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    classes = list(mongo.db.add_class.find())  
    return render_template('classification_config.html', classes=classes)

# Password change page route: Render password change page
@bp.route('/password_change')
def password_change():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('password_change.html')

# Email change page route: Render email change page
@bp.route('/email_change')
def email_change():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('email_change.html')
