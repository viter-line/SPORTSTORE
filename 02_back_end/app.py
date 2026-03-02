"""Головний файл, що збирає всі модулі разом за допомогою Blueprints."""
"""Головний модуль запуску Flask додатку."""
from flask import Flask
from database import db, migrate
from auth import auth_bp
from products import products_bp
from cart import cart_bp
from flask_jwt_extended import JWTManager


def create_app():
    """Фабрика додатку [Clean Architecture]."""
    app = Flask(__name__)

    # Конфігурація MySQL (замініть на власні дані)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:usbw@localhost:3306/sport_store'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sport-store-secure-key'

    # Ініціалізація БД та розширень
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # Реєстрація Blueprint-ів
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)