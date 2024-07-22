from app.routes import bp
from flask import render_template, session, redirect, url_for
from app import mongo
@bp.route('/dashboard')
def dashboard_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    dashboard = mongo.db.dashboard.find_one({'user': session['username']})
    return render_template('dashboard.html', dashboard=dashboard)
