import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as EnumDB, JSON

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

db = SQLAlchemy()


class SaleStatus(Enum):
    PAID = "Paid"
    PENDING = "Pending"
    REFUNDED = "Refunded"
    PROCESSING = "Processing"
    FULFILLED = "Fulfilled"


class Roles(Enum):
    """
    The roles of a user
    Admin will perform all shop administration tasks
    Customer will be the default role
    Sales will be able to create sales or sell to various customers
    """
    ADMIN = "Admin"
    CUSTOMER = "Customer"
    SALES = "Sales"


class PaymentMode(Enum):
    """
    The payment modes
    Mpesa (method1)
    Bank (method2)
    """
    MPESA = "Mpesa"
    BANK = "Bank"


class User(db.Model, UserMixin):
    """
    This model contains all the necessary information about a user. These include:
    User phone, name, password and role. These users must provide phone number and password.
    id: autogenerated id
    phone: user phone number. This will be unique and used to identify a user

    password: User password harsh
    firstname:
    middlename: This is optional
    lastname: First middle and last name will be the names of the user

    registration_date:
    role: The role of the user [ Admin, Tutor, Parent, Student]
    """
    __tablename__ = 'users'
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)  # User Id
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(1000))  # User Password
    firstname = db.Column(db.String)
    middlename = db.Column(db.String)
    lastname = db.Column(db.String)
    role = db.Column(db.String)
    role = Column(db.Enum(Roles), default=Roles.CUSTOMER)
    basket_items = db.relationship("CartItems", backref=db.backref("user", lazy=True))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)


class Inventory(db.Model):
    """
    This model contains information about products.
    id: autogenerated id
    name: product name
    original_price: product original price
    promotion_price: product promotion price
    quantity: product available quantity
    rating: product rating
    description: product description
    image_url: product image url
    weight: product weight
    slug: product slug for SEO purposes
    added_on: product added date

    """
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255))
    original_price = db.Column(db.Float)
    promotion_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    slug = db.Column(db.String(255))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)


class CartItems(db.Model):
    """
    This model contains information about cart items
    id: autogenerated id
    user_id: user id
    inventory_id: product id
    quantity: product quantity
    amount: product amount
    added_on: product added date
    product: product

    """
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Float)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship("Inventory", backref=db.backref("product", lazy=True, uselist=False))


class Sale(db.Model):
    """
    This model contains information about sales
    id: autogenerated id
    served_by: user id
    total: total amount
    bought_by: user id
    discount: discount
    status: sale status
    customer: user
    products: sale products
    added_on: product added date

    """
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    bought_by = db.Column(db.Integer, db.ForeignKey('users.id', name="customer_details"))
    discount = db.Column(db.Float, default=0)
    payment_mode = db.Column(db.Enum(PaymentMode), default=PaymentMode.MPESA)
    status = db.Column(db.Enum(SaleStatus), default=SaleStatus.PENDING)
    customer = db.relationship("User", backref=db.backref('sales', lazy=True), uselist=False,
                               foreign_keys=[bought_by])
    added_on = db.Column(db.DateTime, default=datetime.utcnow)


class SaleData(db.Model):
    """
    This model contains information about sold items
    id: autogenerated id
    sale_price: sale price
    discount: individually applied discount
    inventory_id: product id
    sale_id: sale id
    quantity: product quantity
    added_on: product added date

    """
    __tablename__ = 'sale_data'
    id = db.Column(db.Integer, primary_key=True)
    sale_price = db.Column(db.Float)
    discount = db.Column(db.Float, default=0)  # Individual product discount
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'))
    sale = db.relationship('Sale', backref=db.backref('products', lazy=True))
    quantity = db.Column(db.Integer, default=1)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    inventory = db.relationship("Inventory", backref=db.backref("sale_data", lazy=True))
