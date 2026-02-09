from flask import Blueprint

dishes_bp = Blueprint('dishes', __name__)

from . import routes
