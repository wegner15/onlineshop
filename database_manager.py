from database_models import *
from werkzeug.security import generate_password_hash

from errors_messages import Errors


def db_create_database():
    db.create_all()
    db.reflect()

    # List all table names
    table_names = db.engine.table_names()
    print(table_names)
    print("Database updated successfully")


def db_add_products(name, image_url, weight, quantity, original_price, promotion_price, description, slug=None):
    if not name or not image_url or not weight or not quantity or not original_price or not promotion_price:
        return Errors.MISSING_PARAMS

    if not slug:
        slug = name.replace(" ", "-")

    inventory = Inventory(name=name, image_url=image_url, weight=weight, quantity=quantity,
                          original_price=original_price, promotion_price=promotion_price, description=description,
                          slug=slug)
    db.session.add(inventory)
    db.session.commit()
    return inventory


def db_add_user(first_name, last_name, phone, password):
    if not first_name or not last_name or not phone or not password:
        return Errors.MISSING_PARAMS

    password = generate_password_hash(password)

    user = User(firstname=first_name, lastname=last_name, phone=phone, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def db_get_all_products(lower_bound=None, upper_bound=None):
    if lower_bound and upper_bound:
        products = Inventory.query.filter(Inventory.weight.between(lower_bound, upper_bound)).all()
    elif lower_bound:
        products = Inventory.query.filter(Inventory.weight >= lower_bound).all()
    elif upper_bound:
        products = Inventory.query.filter(Inventory.weight <= upper_bound).all()
    else:
        products = Inventory.query.all()
    return products


def db_get_user_by_phone(phone):
    user = User.query.filter_by(phone=phone).first()
    return user


def db_remove_from_cart(user_id, product_id):
    cart_item = CartItems.query.filter_by(user_id=user_id, inventory_id=product_id).first()
    if not cart_item:
        return False
    db.session.delete(cart_item)
    db.session.commit()

    return True


def db_add_sale(product_id_list, user_id, payment_method):
    if not product_id_list or not user_id:
        return Errors.MISSING_PARAMS

    products_total = 0

    new_sale = Sale(bought_by=user_id, payment_mode=payment_method)
    db.session.add(new_sale)
    db.session.commit()

    for product_id, quantity in product_id_list:

        product = Inventory.query.get(product_id)
        if product:
            products_total += product.promotion_price
            new_sale_data = SaleData(inventory_id=product_id, sale_id=new_sale.id, quantity=quantity)
            db.session.add(new_sale_data)
            db.session.commit()

    new_sale.total = products_total
    db.session.add(new_sale)
    db.session.commit()

    return new_sale


def db_add_to_cart(user_id, product_id, quantity):
    if not user_id or not product_id or not quantity:
        return Errors.MISSING_PARAMS

    # Check if the product is already in cart
    cart_item = CartItems.query.filter_by(user_id=user_id, inventory_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
        db.session.commit()
        return cart_item

    new_cart_item = CartItems(user_id=user_id, inventory_id=product_id, quantity=quantity)
    db.session.add(new_cart_item)
    db.session.commit()
    return new_cart_item
