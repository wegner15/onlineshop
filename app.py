from datetime import timedelta

from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_login import LoginManager, current_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from decouple import config
import click
from flask.cli import with_appcontext

from database_manager import *
from helpers import *
from authentication import auth as authentication_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=300)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
app.config['SECRET_KEY'] = config("SECRET_KEY")

app.register_blueprint(authentication_blueprint, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

IMAGE_UPLOAD_FOLDER = 'static/images'


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


Migrate(app, db, compare_type=True, render_as_batch=True)
db.init_app(app)

csrf = CSRFProtect(app)


@click.command('create_db')
@with_appcontext
def create_db():
    with app.app_context():
        result = create_database()
        click.echo(result)


app.cli.add_command(create_db)

app.jinja_env.filters['commify'] = commify

@app.route('/')
def index():  # put application's code here

    collected_products = db_get_all_products()
    return render_template('index.html', products=collected_products)


@app.route('/products')
def products():
    lower_limit = request.args.get('lower_limit')
    upper_limit = request.args.get('upper_limit')
    collected_products = db_get_all_products(upper_bound=upper_limit, lower_bound=lower_limit)
    return render_template('products.html', products=collected_products, lower_limit=lower_limit,
                           upper_limit=upper_limit)


@app.route("/checkout")
@login_required
def checkout():
    product_list = []
    for product in current_user.basket_items:
        product = [product.product.id, product.quantity]
        product_list.append(product)

    payment_method = request.args.get('payment')

    added_sales = db_add_sale(product_list, current_user.id, payment_method)
    if not added_sales:
        flash("Something went wrong", "error")
        return redirect(url_for("products"))

    for product in current_user.basket_items:
        db_remove_from_cart(current_user.id, product.inventory_id)

    flash("Order confirmed!", "success")
    return redirect(url_for("products"))


@app.route("/orders")
@login_required
def orders():

    return render_template('orders.html')


@app.route("/basket")
@login_required
def cart():
    total_without_promotion = 0
    total_with_promotion = 0
    for item in current_user.basket_items:
        total_without_promotion += item.product.original_price * item.quantity
        total_with_promotion += item.product.promotion_price * item.quantity
    return render_template('cart.html', payment_method=PaymentMode, total_without_promotion=total_without_promotion,
                           total_with_promotion=total_with_promotion)


@app.route("/add-to-cart", methods=['POST'])
@login_required
def add_to_cart():
    payload = request.get_json()
    product_id = payload.get('productId')
    quantity = payload.get('quantity')

    if not product_id or not quantity:
        return jsonify(
            {
                "success": False,
                "message": "Missing required parameters"
            }
        ), 400

    cart_item = db_add_to_cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
    if not cart_item:
        return jsonify(
            {
                "success": False,
                "message": "Failed to add to cart"
            }
        ), 500

    flash("Product added to cart", category='success')
    return jsonify(
        {
            "success": True
        }
    )


@app.route("/add-product", methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        image_url = request.form.get('image_url', type=str)
        image_file = request.files.get('image_file')
        weight = request.form.get('weight', type=float)
        quantity = request.form.get('quantity', type=int, default=1)
        original_price = request.form.get('price', type=float)
        promotion_price = request.form.get('promotional_price', type=float)
        description = request.form.get('description', type=str)

        if not image_url:
            if not image_file:
                flash("Missing some required parameters", category='error')
                return redirect(request.referrer)
            file_upload_path = save_image(IMAGE_UPLOAD_FOLDER, image_file)
            image_url = url_for('static', filename=file_upload_path.replace('\\', '/').replace("static/", ""))

        if not name or not image_url or not weight or not quantity or not original_price or not promotion_price:
            flash("Missing some required parameters", category='error')
            return redirect(request.referrer)

        if promotion_price > original_price:
            flash("Promotion price must be less than original price", category='error')
            return redirect(request.referrer)

        new_product = db_add_products(name, image_url, weight, quantity, original_price, promotion_price, description)
        if new_product == Errors.MISSING_PARAMS:
            flash("Missing some required parameters", category='error')
            return redirect(request.referrer)
        flash("Product created successfully", category='success')
        return redirect(url_for('index'))
    return render_template("admin/add_products.html")


if __name__ == '__main__':
    app.run()
