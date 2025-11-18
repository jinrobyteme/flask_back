from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem

kds_bp = Blueprint('kds_bp', __name__, url_prefix='/api/kds')


@kds_bp.route('/orders', methods=['GET'])
def kds_orders():
    orders = Order.query.filter(Order.status != 'completed').all()
    result = [{"id": o.id, "status": o.status} for o in orders]
    return jsonify(result)


@kds_bp.route('/items/<int:item_id>', methods=['PATCH'])
def update_kds_item(item_id):
    # 구현 생략 (주방 항목 준비 여부 등)
    return jsonify({"message": "Item updated"})


@kds_bp.route('/orders/<int:order_id>', methods=['PATCH'])
def complete_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'completed'
    db.session.commit()
    return jsonify({"message": "Order marked as completed"})


@kds_bp.route('/summary', methods=['GET'])
def kds_summary():
    # 주문 요약 제공용 (필요 시 구현)
    return jsonify({"summary": "Coming soon"})