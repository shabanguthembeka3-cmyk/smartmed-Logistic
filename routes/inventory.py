
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import Inventory, db


# Create Blueprint
inventory_bp = Blueprint(
    'inventory',
    __name__,
    url_prefix='/inventory'
)


@inventory_bp.route('/', methods=['GET', 'POST'])
@login_required
def list_inventory():
    """
    Display inventory items and handle new item creation.

    GET:
        - Fetch all inventory items from database
        - Display them in template

    POST:
        - Get form data
        - Create new inventory record
        - Save to database
        - Redirect to prevent duplicate submission
    """

    # If form is submitted
    if request.method == 'POST':

        # Get data from form
        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        # Create new inventory item
        new_item = Inventory(
            product_name=product_name,
            quantity=quantity,
            price=price
        )

        # Save to database
        db.session.add(new_item)
        db.session.commit()

        # Redirect to inventory page
        return redirect(url_for('inventory.list_inventory'))

    # Get all inventory items
    inventory_items = Inventory.query.all()

    # Render template with data
    return render_template(
        'inventory.html',
        items=inventory_items
    )