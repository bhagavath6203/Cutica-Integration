from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.services import gmail_service,mongo_service