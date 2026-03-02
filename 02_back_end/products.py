"""CRUD операцій для товарів."""
"""Модуль керування каталогом товарів."""
from flask import Blueprint, request, jsonify
from database import db
from models import Product

products_bp = Blueprint('products', __name__, url_prefix='/api')

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Отримання списку всіх товарів."""
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "category": p.category} for p in products])

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """Отримання одного товару за ID."""
    p = Product.query.get_or_404(id)
    return jsonify(id=p.id, name=p.name, description=p.description, price=p.price)

@products_bp.route('/products', methods=['POST'])
def add_product():
    """Додавання нового товару."""
    data = request.json
    new_p = Product(name=data['name'], price=data['price'], category=data['category'], description=data.get('description'))
    db.session.add(new_p)
    db.session.commit()
    return jsonify(message="Product added", id=new_p.id), 201

@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Видалення товару."""
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify(message="Product deleted")