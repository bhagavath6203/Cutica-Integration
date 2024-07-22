from app.routes import bp
from flask import render_template,redirect,url_for,session
from app import mongo
@bp.route('/')
def main_home():
    return render_template('main_home.html')

@bp.route('/account')
def account_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    accounts = mongo.db.account.find_one({'user': session['username']})
    return render_template('account.html', accounts=accounts)

# Notification page route: Render notification page
@bp.route('/notification')
def notification_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    notification = mongo.db.notification.find_one({'user': session['username']})
    return render_template('notification.html', notification=notification)

# Help page route: Render help page
@bp.route('/help')
def help_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    help = mongo.db.help.find_one({'user': session['username']})
    return render_template('help.html', help=help)

# Customers page route: Render customers page
@bp.route('/customers')
def customers_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    customers = mongo.db.customers.find_one({'user': session['username']})
    return render_template('customers.html', customers=customers)

@bp.route('/settings')
def settings_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    settings = mongo.db.settings.find_one({'user': session['username']})
    return render_template('settings.html', settings=settings)
