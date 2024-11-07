# models.py

from flask_sqlalchemy import SQLAlchemy

# Создание экземпляра базы данных SQLAlchemy
db = SQLAlchemy()

# Модель стройматериала
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

# Модель позиции в смете
class EstimateItem(db.Model):
    __tablename__ = 'estimate_items'

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    material = db.relationship('Material', backref='estimate_items')
