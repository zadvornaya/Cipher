from flask import Blueprint

bp = Blueprint('post', __name__, static_folder='static')

from app.post import routes
