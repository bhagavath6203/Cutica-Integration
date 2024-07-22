
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
# from routes.auth import auth
from pymongo.errors import ServerSelectionTimeoutError
from googleapiclient.discovery import build
from oauth2client.client import OAuth2Credentials
from bson.json_util import dumps
from urllib.parse import quote
from bson.errors import InvalidId
import logging
import os
# import secrets
from config import Config
from app.services.mongo_service import get_public_ip, whitelist_ip_in_mongo
from app.services.gmail_service import get_gmail_service, send_email


# from services import gmail_service, mongo_service
# from bson import ObjectId
import base64
from email.mime.text import MIMEText
from dotenv import load_dotenv
from requests.auth import HTTPDigestAuth
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# from app.routes import bp as auth_bp
# Load environment variables from .env file
load_dotenv()
# Initialize Flask application
# app = Flask(__name__)
# app.config.from_object(Config)

mongo = PyMongo()

# app.register_blueprint(auth_bp)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    with app.app_context():
    # Whitelist IP
        current_ip = get_public_ip()
        whitelist_ip_in_mongo(
            current_ip, 
            app.config['ATLAS_API_KEY_PUBLIC'], 
            app.config['ATLAS_API_KEY_PRIVATE'], 
            app.config['ATLAS_GROUP_ID']
        )

        # Initialize Gmail service
        app.gmail_service = get_gmail_service(
            app.config['GOOGLE_CREDENTIALS_PATH'], 
            app.config['GOOGLE_TOKEN_PATH']
        )
        from app.routes import bp as auth_bp
        
        app.register_blueprint(auth_bp)
        # Dashboard page route: Render dashboard page
        # @app.route('/dashboard')
        # def dashboard_page():
        #     if 'username' not in session:
        #         return redirect(url_for('auth.login'))
        #     dashboard = mongo.db.dashboard.find_one({'user': session['username']})
        #     return render_template('dashboard.html', dashboard=dashboard)

        # API route: Get tickets
        # @app.route('/api/tickets', methods=['GET'])
        # def get_tickets():
        #     collection_name = "issues"  # Specify your collection name here
        #     tickets = mongo.db[collection_name].find()
        #     return dumps(tickets)
        # @app.route('/')
        # def main_home():
        #     return render_template('main_home.html')


        # Account page route: Render account page
        # @app.route('/account')
        # def account_page():
        #     if 'username' not in session:
        #         return redirect(url_for('auth.login'))
        #     accounts = mongo.db.account.find_one({'user': session['username']})
        #     return render_template('account.html', accounts=accounts)

        # View class details route with class_id: Render class details page

        # @app.route('/class/<class_id>', methods=['GET', 'POST'])
        # def class_details(class_id):
        #     class_data = mongo.db.classes.find_one({'_id': ObjectId(class_id)})
        #     examples = list(mongo.db.examples.find({'class_id': ObjectId(class_id)}))
            
        #     return render_template('class_details.html', class_details=class_data, examples=examples, class_id=class_id)






        # # Notification page route: Render notification page
        # @app.route('/notification')
        # def notification_page():
        #     if 'username' not in session:
        #         return redirect(url_for('auth.login'))
        #     notification = mongo.db.notification.find_one({'user': session['username']})
        #     return render_template('notification.html', notification=notification)

        # # Help page route: Render help page
        # @app.route('/help')
        # def help_page():
        #     if 'username' not in session:
        #         return redirect(url_for('auth.login'))
        #     help = mongo.db.help.find_one({'user': session['username']})
        #     return render_template('help.html', help=help)

        # # Customers page route: Render customers page
        # @app.route('/customers')
        # def customers_page():
        #     if 'username' not in session:
        #         return redirect(url_for('auth.login'))
        #     customers = mongo.db.customers.find_one({'user': session['username']})
        #     return render_template('customers.html', customers=customers)


    return app
# # Function to get current public IP address
# def get_public_ip():
#     response = requests.get("https://api.ipify.org")
#     return response.text

# # Function to whitelist IP in MongoDB Atlas access list
# def whitelist_ip_in_mongo(ip):
#     try:
#         atlas_api_key_public = os.getenv('ATLAS_API_KEY_PUBLIC')
#         atlas_api_key_private = os.getenv('ATLAS_API_KEY_PRIVATE')
#         atlas_group_id = os.getenv('ATLAS_GROUP_ID')
#         resp = requests.post(
#             f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList",
#             auth=HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
#             json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]
#         )
#         if resp.status_code in (200, 201):
#             print("MongoDB Atlas accessList request successful", flush=True)
#         else:
#             print(
#                 f"MongoDB Atlas accessList request problem: status code was {resp.status_code}, content was {resp.content}",
#                 flush=True
#             )
#     except Exception as e:
#         print(f"Error while whitelisting IP in MongoDB Atlas: {str(e)}")

# Get current public IP and whitelist it in MongoDB Atlas
# current_ip = get_public_ip()
# whitelist_ip_in_mongo(current_ip)

# Whitelist IP in MongoDB Atlas
# current_ip = get_public_ip()
# whitelist_ip_in_mongo(current_ip, app.config['ATLAS_API_KEY_PUBLIC'], app.config['ATLAS_API_KEY_PRIVATE'], app.config['ATLAS_GROUP_ID'])

# # Initialize Gmail service
# gmail_service = get_gmail_service(app.config['GOOGLE_CREDENTIALS_PATH'], app.config['GOOGLE_TOKEN_PATH'])


# # Google API Client Libraries setup (authentication)
# SCOPES = ['https://www.googleapis.com/auth/gmail.send']
# creds = None

# # Paths for credentials and tokens
# current_dir = os.path.dirname(os.path.abspath(__file__))
# auth_dir = os.path.join(current_dir, 'auth')
# credentials_path = os.path.join(auth_dir, 'credentials.json')
# token_path = os.path.join(auth_dir, 'token.pickle')

# # Load credentials from token or request new ones if needed
# if os.path.exists(token_path):
#     with open(token_path, 'rb') as token:
#         creds = pickle.load(token)

# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
#         creds = flow.run_local_server(port=0)
#     with open(token_path, 'wb') as token:
#         pickle.dump(creds, token)

# # Build Gmail service
# service = build('gmail', 'v1', credentials=creds)

# # Function to send email using Gmail API
# def send_email(to, subject, body):
#     message = MIMEText(body)
#     message['to'] = to
#     message['subject'] = subject
#     raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
#     message = {'raw': raw}
#     try:
#         message = (service.users().messages().send(userId='me', body=message).execute())
#         print('Message Id: %s' % message['id'])
#         return message
#     except Exception as error:
#         print(f'An error occurred: {error}')
#         return None

# Main route: Render main home page
# @app.route('/')
# def main_home():
#     return render_template('main_home.html')

# # Login page route: Render login page
# @app.route('/login')
# def auth.login():
#     return render_template('login.html')

# # Signup page route: Render signup page
# @app.route('/signup')
# def signup_page():
#     return render_template('signup.html')

# # Forgot password page route: Render forgot password page
# @app.route('/forgot_password')
# def forgot_password_page():
#     return render_template('forgot_password.html')

# # Reset password route with token: Handle reset password functionality
# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     user = mongo.db.password_resets.find_one({'token': token})
#     if not user:
#         flash('Invalid or expired token', 'danger')
#         return redirect(url_for('auth.login'))
    
#     if request.method == 'POST':
#         new_password = request.form.get('newPassword')
#         mongo.db.users.update_one({'email': user['email']}, {'$set': {'password': new_password}})
#         mongo.db.password_resets.delete_one({'token': token})
#         flash('Your password has been updated!', 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('reset_password.html', token=token)

# # Home route with username: Render home page
# @app.route('/home/<username>')
# def home(username):
#     return render_template('home.html', username=username)

# # Login POST request route: Handle user login
# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         email = request.form.get('loginEmail')
#         password = request.form.get('loginPassword')
#         user = mongo.db.users.find_one({'email': email})
#         if user:
#             session['username'] = user['username']
#             session['email'] = email
#             session['role'] = user.get('role', 'user')
#             if user['password'] == password:
#                 flash('Login successful!', 'success')
#                 if session['role'] == 'admin':
#                     return redirect(url_for('dashboard_page'))  # Correct endpoint name
#                 else:
#                     return redirect(url_for('home', username=user['username']))
#             else:
#                 flash('Wrong password. Please try again.', 'danger')
#                 return redirect(url_for('auth.login'))
#         else:
#             flash('Invalid email. Please try again.', 'danger')
#             return redirect(url_for('auth.login'))
#     except ServerSelectionTimeoutError:
#         flash('Could not connect to MongoDB. Please try again later.', 'danger')
#         return redirect(url_for('auth.login'))


# # Dashboard page route: Render dashboard page
# @app.route('/dashboard')
# def dashboard_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     dashboard = mongo.db.dashboard.find_one({'user': session['username']})
#     return render_template('dashboard.html', dashboard=dashboard)

# # API route: Get tickets
# @app.route('/api/tickets', methods=['GET'])
# def get_tickets():
#     collection_name = "issues"  # Specify your collection name here
#     tickets = mongo.db[collection_name].find()
#     return dumps(tickets)


# # Account page route: Render account page
# @app.route('/account')
# def account_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     accounts = mongo.db.account.find_one({'user': session['username']})
#     return render_template('account.html', accounts=accounts)

# # View class details route with class_id: Render class details page

# @app.route('/class/<class_id>', methods=['GET', 'POST'])
# def class_details(class_id):
#     class_data = mongo.db.classes.find_one({'_id': ObjectId(class_id)})
#     examples = list(mongo.db.examples.find({'class_id': ObjectId(class_id)}))
    
#     return render_template('class_details.html', class_details=class_data, examples=examples, class_id=class_id)






# # Notification page route: Render notification page
# @app.route('/notification')
# def notification_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     notification = mongo.db.notification.find_one({'user': session['username']})
#     return render_template('notification.html', notification=notification)

# # Help page route: Render help page
# @app.route('/help')
# def help_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     help = mongo.db.help.find_one({'user': session['username']})
#     return render_template('help.html', help=help)

# # Customers page route: Render customers page
# @app.route('/customers')
# def customers_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     customers = mongo.db.customers.find_one({'user': session['username']})
#     return render_template('customers.html', customers=customers)

# # Signup POST request route: Handle user signup
# @app.route('/signup', methods=['POST'])
# def signup():
#     try:
#         username = request.form.get('signUpUsername')
#         email = request.form.get('signUpEmail')
#         password = request.form.get('signUpPassword')
#         user = mongo.db.users.find_one({'email': email})
#         if user:
#             flash('Email already exists', 'danger')
#             return redirect(url_for('signup_page'))
#         else:
#             mongo.db.users.insert_one({'username': username, 'email': email, 'password': password, 'role': 'admin'})
#             flash('Sign up successful!', 'success')
#             return redirect(url_for('auth.login'))
#     except ServerSelectionTimeoutError:
#         flash('Could not connect to MongoDB. Please try again later.', 'danger')
#         return redirect(url_for('signup_page'))

# # Forgot password POST request route: Handle forgot password functionality
# @app.route('/forgot_password', methods=['POST'])
# def forgot_password():
#     try:
#         email = request.form.get('forgotPasswordEmail')
#         user = mongo.db.users.find_one({'email': email})
#         if user:
#             token = secrets.token_urlsafe(32)
#             mongo.db.password_resets.insert_one({'email': email, 'token': token})
#             reset_url = url_for('reset_password', token=token, _external=True)
#             subject = 'Password Reset Request'
#             body = f'Click the link to reset your password: {reset_url}'
#             send_email(gmail_service,email, subject, body)
#             flash('A password reset link has been sent to your email.', 'info')
#         else:
#             flash('Email not found', 'danger')
#         return redirect(url_for('forgot_password_page'))
#     except ServerSelectionTimeoutError:
#         flash('Could not connect to MongoDB. Please try again later.', 'danger')
#     return redirect(url_for('forgot_password_page'))

# # Settings page route: Render settings page
# @app.route('/settings')
# def settings_page():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     settings = mongo.db.settings.find_one({'user': session['username']})
#     return render_template('settings.html', settings=settings)

# Support team page route: Render support team page
# @app.route('/support_team')
# def support_team():
#     admin_email = session.get('email')
#     support_members = mongo.db.support_team.find({'admin_email': admin_email})
#     return render_template('support_team.html', support_members=support_members)

# # Add support member page route: Render add support member page
# @app.route('/add_support')
# def add_support():
#     return render_template('add_support.html')

# # Add class page route: Render add class page
# @app.route('/add_class')
# def add_class():
#     return render_template('add_class.html')

# # Email configuration page route: Render email configuration page
# @app.route('/email_config')
# def email_config():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     return render_template('email_config.html')

# # Classification configuration page route: Render classification configuration page
# @app.route('/classification_config')
# def classification_config():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))

#     classes = list(mongo.db.add_class.find())  
#     return render_template('classification_config.html', classes=classes)

# # Password change page route: Render password change page
# @app.route('/password_change')
# def password_change():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     return render_template('password_change.html')

# # Email change page route: Render email change page
# @app.route('/email_change')
# def email_change():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     return render_template('email_change.html')

# # Add support credentials POST request route: Handle adding new support credentials
# @app.route('/new_support_credentials', methods=['POST'])
# def new_support_credentials():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     phone = request.form.get('phone')
#     admin_email = session.get('email')

#     # Generate random password and support ID
#     password = secrets.token_urlsafe(12)
#     support_id = secrets.randbelow(1000)  # Generate a random support ID (0-999)

#     # Insert support member into users collection
#     mongo.db.users.insert_one({'username': name, 'email': email, 'password': password, 'role': 'support'})

#     # Insert support member details into support_team collection
#     mongo.db.support_team.insert_one({'support_id': support_id, 'name': name, 'email': email, 'phone': phone, 'admin_email': admin_email})

#     # Send email with credentials
#     subject = 'Your Support Account Credentials'
#     body = f'Username: {email}\nPassword: {password}\nSupport ID: {support_id}'
#     send_email(gmail_service, email, subject, body)

#     flash('Support member added and credentials sent!', 'success')
#     return redirect(url_for('support_team'))

# # Add class credentials POST request route: Handle adding new class credentials
# @app.route('/new_class_credentials', methods=['POST'])
# def new_class_credentials():
#     # Retrieve data from the POST request
#     name = request.form.get('name')
#     description = request.form.get('description')

#     class_id = secrets.randbelow(1000)  # Generate a random class_id

#     # Insert class details into 'add_class' collection in MongoDB
#     mongo.db.add_class.insert_one({'class_id': class_id, 'class_name': name, 'description': description})

#     # Flash message for success and redirect to classification_config route
#     flash('Class added successfully', 'success')
#     return redirect(url_for('classification_config'))

# # Delete class route with class_id: Handle deleting class
# @app.route('/delete_class/<class_id>', methods=['DELETE'])
# def delete_class(class_id):
#     try:
#         result = mongo.db.add_class.delete_one({'class_id': int(class_id)})
#         if result.deleted_count == 1:
#             return jsonify({'success': True}), 200
#         else:
#             return jsonify({'success': False, 'error': 'Class not found'}), 404
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
    


# @app.route('/view_class_details/<class_id>')
# def view_class_details(class_id):
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))

#     try:
#         class_details = mongo.db.add_class.find_one({'class_id': int(class_id)})
#         if not class_details:
#             flash('Class not found', 'danger')
#             return render_template('view_class_details.html', class_details=None, examples=None, autoresponses=None)

#         examples = list(mongo.db.examples.find({'class_id': int(class_id)}))
#         autoresponses = list(mongo.db.autoresponses.find({'class_id': int(class_id)}))
#         return render_template('view_class_details.html', class_details=class_details, examples=examples, autoresponses=autoresponses)
#     except Exception as e:
#         flash(f'An error occurred: {e}', 'danger')
#         return render_template('view_class_details.html', class_details=None, examples=None, autoresponses=None)




# @app.route('/add_example/<int:class_id>', methods=['POST'])
# def add_example(class_id):
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     example_data = request.form.get('example_data')

#     if not example_data:
#         return jsonify({'success': False, 'error': 'Example is required'}), 400

#     try:
#         mongo.db.examples.insert_one({
#             'class_id': class_id,
#             'example_data': example_data,
#         })
#         return jsonify({'success': True, 'message': 'Example added successfully'}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
    

# @app.route('/add_autoresponse/<int:class_id>', methods=['POST'])
# def add_autoresponse(class_id):
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     autoresponse_data = request.form.get('autoresponse_data')

#     if not autoresponse_data:
#         return jsonify({'success': False, 'error': 'Autoresponse is required'}), 400

#     try:
#         mongo.db.autoresponses.insert_one({
#             'class_id': class_id,
#             'response': autoresponse_data,
#         })
#         return jsonify({'success': True, 'message': 'Autoresponse added successfully'}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
    


# @app.route('/edit_example/<class_id>/<example_id>', methods=['POST'])

# def edit_example(class_id, example_id):
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     data = request.json
#     new_example_data = data.get('data')

#     if not new_example_data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     try:
#         result = mongo.db.examples.update_one(
#             {'_id': ObjectId(example_id), 'class_id': int(class_id)},
#             {'$set': {'example_data': new_example_data}}
#         )
#         if result.modified_count == 1:
#             return jsonify({'success': True, 'message': 'Example updated successfully'}), 200
#         else:
#             return jsonify({'success': False, 'error': 'Example not found or not modified'}), 404
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/delete_example', methods=['POST'])
# def delete_example():
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     data = request.json
#     class_id = data.get('class_id')
#     example_id = data.get('id')

#     try:
#         result = mongo.db.examples.delete_one({
#             '_id': ObjectId(example_id),
#             'class_id': int(class_id)
#         })
#         if result.deleted_count == 1:
#             return jsonify({'success': True, 'message': 'Example deleted successfully'}), 200
#         else:
#             return jsonify({'success': False, 'error': 'Example not found'}), 404
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/edit_autoresponse/<class_id>/<autoresponse_id>', methods=['POST'])
# def edit_autoresponse(class_id, autoresponse_id):
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     data = request.json
#     new_autoresponse_data = data.get('data')

#     if not new_autoresponse_data:
#         return jsonify({'success': False, 'error': 'No data provided'}), 400

#     try:
#         result = mongo.db.autoresponses.update_one(
#             {'_id': ObjectId(autoresponse_id), 'class_id': int(class_id)},
#             {'$set': {'response': new_autoresponse_data}}
#         )
#         if result.modified_count == 1:
#             return jsonify({'success': True, 'message': 'Autoresponse updated successfully'}), 200
#         else:
#             return jsonify({'success': False, 'error': 'Autoresponse not found or not modified'}), 404
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/delete_autoresponse', methods=['POST'])
# def delete_autoresponse():
#     if 'username' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     data = request.json
#     class_id = data.get('class_id')
#     autoresponse_id = data.get('id')

#     try:
#         result = mongo.db.autoresponses.delete_one({
#             '_id': ObjectId(autoresponse_id),
#             'class_id': int(class_id)
#         })
#         if result.deleted_count == 1:
#             return jsonify({'success': True, 'message': 'Autoresponse deleted successfully'}), 200
#         else:
#             return jsonify({'success': False, 'error': 'Autoresponse not found'}), 404
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500


# # Logout route: Handle user logout
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('auth.login'))

# # Run the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)
