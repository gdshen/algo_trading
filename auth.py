import logging

from flask import Blueprint, redirect, request, render_template, flash
from flask_login import current_user, login_user, logout_user

from app import flask_bcrypt, login_manager
from forms import LoginForm, SignupForm
from user import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')


@auth_flask_login.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        flash("You have login before, return to homepage!")
        return redirect('/')
    form = LoginForm(request.form)
    if request.method == 'POST':
        user_obj = User()
        email = form.email.data
        password = form.password.data
        user_obj.get_by_email(email, password_acquirement=True)
        if flask_bcrypt.check_password_hash(user_obj.password, password):
            login_user(user_obj)
            flash("Logged in!")
        else:
            logging.debug('login-- user {} has input wrong password'.format(email))
        return redirect('/')
    return render_template('login.html', form=form)


@auth_flask_login.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user_obj = User()
            email = form.email.data
            password = flask_bcrypt.generate_password_hash(form.password.data)
            user_obj.email = email
            user_obj.password = password
            user_id = user_obj.save() # user_id will be none if email has already been registered
            if not user_id:
                flash('Email has already been registered!')
                return redirect('/register')
            logging.debug('Register-- {} registered'.format(email))
            return redirect('/login')
        else:
            logging.debug('Register-- validate check failed')
            flash("Information input error, please input again!")
    return render_template('register.html', form=form)


@auth_flask_login.route('/logout')
def logout():
    logout_user()
    flash('Logged out!')
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    """ deal with anonymous users access to pages that need login """
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    """ user_loader is required by flask_login extension to load user

    :param user_id: unicode of user_id
    :return: user: User or None
    """
    if user_id is None:
        redirect('/login')
    user = User()
    user.get_by_id(user_id)
    if user.is_active:
        return user
    else:
        return None
