from flask import Blueprint, jsonify
from models import MenuItem

menu_bp = Blueprint('menu_bp', __name__, url_prefix='/api/menu')

@menu_bp.route('', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    result = [{"id": item.id, "name": item.name, "price": item.price} for item in items]
    return jsonify(result), 200