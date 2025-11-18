from flask import Blueprint, jsonify
from models import db, Payment, Order, OrderItem, MenuItem
from datetime import datetime

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/api/pay')


@payment_bp.route('/<int:order_id>', methods=['GET'])
def get_payment_info(order_id):
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return jsonify({"message": "No payment yet"}), 404

    # 주문 총액 계산
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    total_price = sum(item.quantity * item.menu_item.price for item in order_items)

    return jsonify({
        "declared": payment.is_declared,
        "verified": payment.is_verified,
        "declared_at": payment.declared_at,
        "verified_at": payment.verified_at,
        "total_price": total_price
    })


@payment_bp.route('/<int:order_id>/declare', methods=['POST'])
def declare_payment(order_id):
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        payment = Payment(order_id=order_id, is_declared=True, declared_at=datetime.utcnow())
        db.session.add(payment)
    else:
        payment.is_declared = True
        payment.declared_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Payment declared"})


@payment_bp.route('/<int:order_id>/verify', methods=['POST'])
def verify_payment(order_id):
    payment = Payment.query.filter_by(order_id=order_id).first_or_404()
    payment.is_verified = True
    payment.verified_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Payment verified"})