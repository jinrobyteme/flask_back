from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#유저 테이블
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(20), unique = True, nullable = False)

    def __repr__(self):
        return f'<User {self.name}, {self.phone}>'

# 메뉴 테이블
class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)

    def __repr__(self):
        return f'<MenuItem {self.name}, {self.price}>'


# 주문 테이블
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')

    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False)

    def __repr__(self):
        return f'<Order {self.id}, Status: {self.status}>'


# 주문 항목 테이블
class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id}, Item:{self.item_id}, Qty:{self.quantity}>'


# 결제 테이블
class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    is_declared = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    declared_at = db.Column(db.DateTime)
    verified_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Payment Order:{self.order_id}, Verified:{self.is_verified}>'