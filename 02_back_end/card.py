"""Логіка кошика та розрахунок загальної вартості(Total)."""
"""Модуль керування кошиком покупок."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Cart, CartItem, Product

cart_bp = Blueprint('cart', __name__, url_prefix='/api')


@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Перегляд кошика та розрахунок загальної суми."""
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    items = []
    total = 0
    for item in cart.items:
        p = Product.query.get(item.product_id)
        subtotal = p.price * item.quantity
        total += subtotal
        items.append(
            {"id": item.id, "product": p.name, "price": p.price, "quantity": item.quantity, "subtotal": subtotal})
    return jsonify(items=items, total_price=round(total, 2))


@cart_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Додавання товару до кошика."""
    user_id = get_jwt_identity()
    data = request.json
    cart = Cart.query.filter_by(user_id=user_id).first()

    new_item = CartItem(cart_id=cart.id, product_id=data['product_id'], quantity=data.get('quantity', 1))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(message="Added to cart"), 201


@cart_bp.route('/cart/remove/<int:id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(id):
    """Видалення елемента з кошика."""
    item = CartItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(message="Removed from cart")