from flask import Blueprint, render_template, redirect, url_for, request, flash

from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import session as Session
from werkzeug.security import check_password_hash

from database_manager import *

auth = Blueprint('auth', __name__)


def redirect_dest(fallback):
    dest = Session.get('next')
    try:
        if dest:
            return redirect(dest)

    except:
        return redirect(fallback)
    return redirect(fallback)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    dest = request.args.get('next')
    Session['next'] = dest
    Session.modified = True
    if request.method == 'POST':
        password = request.form.get('password')
        phone = request.form.get('phone')

        user = db_get_user_by_phone(phone)
        if not user:
            flash("Check your phone or password and try again", category='error')
            return redirect(request.referrer)
        if not check_password_hash(user.password, password):
            flash("Check your phone or password and try again", category='error')
            return redirect(request.referrer)
        login_user(user, remember=True)
        flash(f"Welcome {current_user.lastname}!", category='success')
        return redirect_dest('/')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = request.form.get('password')
        repeat_password = request.form.get('repeatPassword')
        phone = request.form.get('phone')

        if not first_name or not last_name or not phone or not password:
            flash("Missing some required parameters")
            return redirect(request.referrer)

        if not password == repeat_password:
            flash("Passwords don't match")
            return redirect(request.referrer)

        new_user = db_add_user(first_name, last_name, phone, password)
        if new_user == Errors.MISSING_PARAMS:
            flash("Missing some required parameters", category='error')
            return redirect(request.referrer)
        flash("User created successfully", category='success')
        login_user(new_user)

        return redirect_dest('/')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
