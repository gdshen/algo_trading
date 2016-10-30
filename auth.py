import logging

from flask import redirect, request, render_template, flash
from flask_login import current_user, login_user, logout_user

from app import app, flask_bcrypt, login_manager
from forms import LoginForm, SignupForm
from user import User


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user_obj = User()
            email = form.email.data
            password = flask_bcrypt.generate_password_hash(form.password.data)
            user_obj.email = email
            user_obj.password = password
            user_obj.save()
            # todo: protect registered email register again
            logging.debug('Register-- {} registered'.format(email))
            return redirect('/login')
        else:
            logging.debug('Register-- validate check failed')
            flash("Information input error, please input again!")
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
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
