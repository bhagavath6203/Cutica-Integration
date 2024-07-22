from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.routes import auth, dashboard, main, support, classification, settings