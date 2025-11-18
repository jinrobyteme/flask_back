from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/orders')


@order_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    items = data.get('items')  # [{item_id: 1, quantity: 2}, ...]

    new_order = Order(user_id=user_id, status='pending')
    db.session.add(new_order)
    db.session.flush()  # order.id 생성됨

    for item in items:
        order_item = OrderItem(order_id=new_order.id,
                               item_id=item['item_id'],
                               quantity=item['quantity'])
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"message": "Order created", "order_id": new_order.id}), 201


@order_bp.route('/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    data = request.get_json()
    status = data.get('status')

    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    return jsonify({"message": "Order status updated"})