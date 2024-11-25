from flask import Blueprint

main = Blueprint('main', __name__)

from . import users, categories, products, orders, order_details, reviews, suppliers, purchases, payments   