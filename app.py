from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, User, Inventory, Order
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

from flask import redirect, url_for

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    ...


# Register Blueprints Here
from routes.inventory import inventory_bp
app.register_blueprint(inventory_bp)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

# Create default admin
with app.app_context():
    db.create_all()


# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    total_inventory = Inventory.query.count()
    total_orders = Order.query.count()

    return render_template(
        'dashboard.html',
        total_inventory=total_inventory,
        total_orders=total_orders
    )

# LOGIN

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')

# REGISTER

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("User created successfully")
        return redirect(url_for('login'))

    return render_template('register.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# INVENTORY
@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    if request.method == 'POST':
        new_item = Inventory(
            product_name=request.form['product_name'],
            quantity=request.form['quantity'],
            price=request.form['price']
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('inventory'))

    #  SEARCH FUNCTION
    search = request.args.get('search')

    if search:
        items = Inventory.query.filter(
            Inventory.product_name.ilike(f"%{search}%")
        ).all()
    else:
        items = Inventory.query.all()

    return render_template('inventory.html', items=items)
@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    if request.method == 'POST':
        new_order = Order(
            product_name=request.form['product_name'],
            quantity=request.form['quantity'],
            status=request.form['status']
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('orders'))

    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)

@app.route('/delete_order/<int:id>')
@login_required
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)