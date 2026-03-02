"""Модуль для ініціалізації SQLAlchemy та Migrate."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()