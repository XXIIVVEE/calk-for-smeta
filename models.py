# models.py

from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

# Модель для пользователя
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), unique=True, nullable=False)

    # Связь с записями сметы
    estimate_items = db.relationship('EstimateItem', backref='user', lazy=True)


# Модель для материала
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)


# Модель для позиции в смете
class EstimateItem(db.Model):
    __tablename__ = 'estimate_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    material = db.relationship('Material', backref='estimate_items')


# Функция для добавления материалов в базу, если их ещё нет
def seed_materials(app):
    with app.app_context():
        if not Material.query.first():  # Проверяем, есть ли уже материалы
            materials = [
                Material(name="Кирпич", unit_price=35, unit="штука"),
                Material(name="Цемент", unit_price=700, unit="мешок"),
                Material(name="Краска", unit_price=1600, unit="литр"),
                Material(name="Доска", unit_price=50, unit="метр"),
                Material(name="Штукатурка", unit_price=400, unit="мешок"),
                Material(name="Гипсокартон", unit_price=250, unit="лист"),
                Material(name="Плитка", unit_price=600, unit="кв. м"),
                Material(name="Арматура", unit_price=90, unit="метр"),
                Material(name="Песок", unit_price=1000, unit="куб. м"),
                Material(name="Щебень", unit_price=700, unit="куб. м"),
            ]
            db.session.add_all(materials)
            db.session.commit()


# Функция поиска более дешёвых предложений с заглушками на реальные сайты
def find_cheaper_price(material_name, current_price):
    # Примеры ссылок на материалы (замените на реальные ссылки при необходимости)
    example_sites = [
        {"site": "Leroy Merlin", "url": "https://leroymerlin.ru/search/?q=" + material_name.replace(" ", "+")},
        {"site": "Ozon", "url": "https://www.ozon.ru/search/?text=" + material_name.replace(" ", "+")},
        {"site": "Wildberries", "url": "https://www.wildberries.ru/catalog/0/search.aspx?search=" + material_name.replace(" ", "+")},
    ]
    
    cheaper_options = []
    
    # Создание нескольких вариантов с ценами, случайно немного ниже текущей
    for site in example_sites:
        random_price = round(random.uniform(0.7, 0.95) * current_price, 2)
        cheaper_options.append({"site": site["site"], "price": random_price, "url": site["url"]})
    
    # Возвращаем только те предложения, которые дешевле текущей цены
    return [option for option in cheaper_options if option["price"] < current_price]