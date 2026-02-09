from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .auth import auth_bp
from .users import users_bp
from .ingredients import ingredients_bp
from .suppliers import suppliers_bp
from .dishes import dishes_bp
from .menus import menus_bp
from .orders import orders_bp
from .employees import employees_bp
from .financial import financial_bp
from .mother_baby import mother_baby_bp
from .system import system_bp

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(ingredients_bp, url_prefix='/ingredients')
api_bp.register_blueprint(suppliers_bp, url_prefix='/suppliers')
api_bp.register_blueprint(dishes_bp, url_prefix='/dishes')
api_bp.register_blueprint(menus_bp, url_prefix='/menus')
api_bp.register_blueprint(orders_bp, url_prefix='/orders')
api_bp.register_blueprint(employees_bp, url_prefix='/employees')
api_bp.register_blueprint(financial_bp, url_prefix='/financial')
api_bp.register_blueprint(mother_baby_bp, url_prefix='/mother-baby')
api_bp.register_blueprint(system_bp, url_prefix='/system')
