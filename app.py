# app.py

from flask import Flask, render_template, request, redirect, url_for
from models import db, Material, EstimateItem, User, seed_materials, find_cheaper_price

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Создание таблиц и добавление материалов при запуске
with app.app_context():
    db.create_all()
    seed_materials(app)

# Функция для получения или создания пользователя на основе IP-адреса
def get_or_create_user(ip_address):
    user = User.query.filter_by(ip_address=ip_address).first()
    if not user:
        user = User(ip_address=ip_address)
        db.session.add(user)
        db.session.commit()
    return user

@app.route('/')
def index():
    materials = Material.query.all()
    return render_template('index.html', materials=materials)

@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    ip_address = request.remote_addr
    user = get_or_create_user(ip_address)
    
    if request.method == 'POST':
        material_id = int(request.form['material_id'])
        quantity = int(request.form['quantity'])

        estimate_item = EstimateItem.query.filter_by(user_id=user.id, material_id=material_id).first()
        
        if estimate_item:
            estimate_item.quantity += quantity
            estimate_item.total_cost = estimate_item.quantity * estimate_item.material.unit_price
        else:
            material = Material.query.get(material_id)
            total_cost = material.unit_price * quantity
            estimate_item = EstimateItem(user_id=user.id, material_id=material_id, quantity=quantity, total_cost=total_cost)
            db.session.add(estimate_item)

        db.session.commit()

    estimate_items = EstimateItem.query.filter_by(user_id=user.id).all()
    total_estimate = sum(item.total_cost for item in estimate_items)
    materials = Material.query.all()
    cheaper_prices = {
        item.material.name: find_cheaper_price(item.material.name, item.material.unit_price)
        for item in estimate_items
    }

    return render_template('estimate.html', estimate_items=estimate_items, total_estimate=total_estimate, materials=materials, cheaper_prices=cheaper_prices)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = EstimateItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('estimate'))

@app.route('/clear')
def clear():
    ip_address = request.remote_addr
    user = get_or_create_user(ip_address)
    EstimateItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return redirect(url_for('estimate'))

# app.py

from flask import Flask, render_template

app = Flask(__name__)

# Маршрут для страницы чертежа
@app.route('/drawing')
def drawing():
    return render_template('drawing.html')

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
