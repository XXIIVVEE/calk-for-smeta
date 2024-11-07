from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Material, EstimateItem

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Функция для создания таблиц при старте приложения
def create_tables():
    with app.app_context():
        db.create_all()

# Запуск создания таблиц при старте приложения
create_tables()

@app.route('/')
def index():
    materials = Material.query.all()  # Получаем все материалы из базы
    return render_template('index.html', materials=materials)
def add_material():
    # Получаем данные из формы
    name = request.form['name']
    unit_price = float(request.form['unit_price'])
    unit = request.form['unit']

    # Добавляем материал в базу данных
    new_material = Material(name=name, unit_price=unit_price, unit=unit)
    db.session.add(new_material)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    if request.method == 'POST':
        material_id = int(request.form['material_id'])
        quantity = int(request.form['quantity'])

        # Находим материал и вычисляем стоимость
        material = Material.query.get(material_id)
        total_cost = material.unit_price * quantity

        # Добавляем запись в таблицу EstimateItem
        estimate_item = EstimateItem(material_id=material_id, quantity=quantity, total_cost=total_cost)
        db.session.add(estimate_item)
        db.session.commit()

    # Получаем все позиции сметы для отображения
    estimate_items = EstimateItem.query.all()
    total_estimate = sum(item.total_cost for item in estimate_items)
    return render_template('estimate.html', estimate_items=estimate_items, total_estimate=total_estimate)

@app.route('/clear')
def clear():
    # Очищаем смету
    EstimateItem.query.delete()
    db.session.commit()
    return redirect(url_for('estimate'))

if __name__ == '__main__':
    app.run(debug=True)
