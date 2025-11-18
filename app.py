from flask import Flask, request, jsonify
from models import db
from routes import order_bp, menu_bp, payment_bp, kds_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydb.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/users')
def users():
    return jsonify({"members": [{ "id" : 1, "name" : "yerin" }, { "id" : 2, "name" : "dalkong" }]})
           
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(order_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(kds_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)