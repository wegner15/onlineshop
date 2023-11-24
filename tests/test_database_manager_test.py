
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

from app import app
from database_manager import *


@pytest.fixture(scope='module')
def test_app():
    # app = create_app('testing')
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_db(test_app):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


def test_db_add_user(test_app, test_db):
    user = db_add_user("John", "Doe", "1234567890", "password")
    assert user is not None
    assert user.firstname == "John"
    assert user.phone == "1234567890"


def test_db_get_all_products(test_app, test_db):
    # First, add a product
    db_add_products("Test Product", "image_url", 10, 5, 100.0, 80.0, "description")
    products = db_get_all_products()
    assert len(products) == 1
    assert products[0].name == "Test Product"


def test_db_get_user_by_phone(test_app, test_db):
    db_add_user("Jane", "Doe", "9876543210", "password")
    user = db_get_user_by_phone("9876543210")
    assert user is not None
    assert user.phone == "9876543210"


def test_db_add_to_cart(test_app, test_db):
    # Add user and product first
    user = db_add_user("Alice", "Wonderland", "1112223333", "password")
    product = db_add_products("Widget", "url", 1, 10, 20.0, 15.0, "A widget")
    cart_item = db_add_to_cart(user.id, product.id, 2)
    assert cart_item is not None
    assert cart_item.quantity == 2


def test_db_remove_from_cart(test_app, test_db):
    # Setup: Add user, product, and then add to cart
    user = db_add_user("Bob", "Builder", "2223334444", "password")
    product = db_add_products("Gadget", "url", 2, 20, 30.0, 25.0, "A gadget")
    db_add_to_cart(user.id, product.id, 1)

    # Test removal
    result = db_remove_from_cart(user.id, product.id)
    assert result is True


def test_db_add_sale(test_app, test_db):
    # Add user and products
    user = db_add_user("Eve", "Online", "3334445555", "password")
    product = db_add_products("Thing", "url", 3, 30, 40.0, 35.0, "A thing")

    # Create a sale
    sale = db_add_sale([(product.id, 1)], user.id, PaymentMode.MPESA)
    assert sale is not None
    assert sale.total == product.promotion_price
