"""
This is the entry point for the app 
"""

import os
from flask import request, redirect, url_for,\
    render_template, flash
from app import create_app
from app.models import db
from app import controller

config_name = os.getenv('APP_SETTINGS') or 'development'
app = create_app(config_name)
    

# routes
@app.route('/')
def index():
    """
    The homepage comprising signup and signin options
    """
    active = 'home'
    return render_template('index.html', active=active)


@app.route('/signup', methods=['POST'])
def signup():
    """
    The signup route handles POST data sent from 
    the signup form on the home/index page
    """
    error = None
    form_data = None
    try:
        required_keys = ('first_name', 'last_name', 'email', 'password')
        form_data = controller.process_form_data(dict(request.form),
                                                 *required_keys)
    except (AttributeError, ValueError):
        error = 'invalid request'
    if form_data:
        # get the data and attempt to create a new user
        try:
            user = db.create_user(form_data)            
        except ValueError as e:
            # error = 'Invalid form input'
            error = str(e)
        else:
            # if new user is created, log them in
            try:
                controller.add_user_to_session(user.key)
            except KeyError:
                error = 'Error while logging in'
            else:
                # redirect the user to dashboard
                flash('User sign up successful')

                # return app.models.users
                return redirect(url_for('categories_list',
                                user_key=user.key))
    if error:
        flash(error)
    return redirect(url_for('index'))



@app.route('/signout')
def signout():
    """
    The signout route logs out the user
    """
    error = None
    # remove user_key from session
    try:
        controller.remove_user_from_session()
    except KeyError:
        error = 'You are not logged in'
    if error:
        flash(error)
    return redirect(url_for('index'))


@app.route('/signin', methods=['POST'])
def signin():
    """
    Logs in the user
    """
    error = None
    form_data = None
    # get request.form data
    try:
        required_keys = ('email', 'password')
        form_data = controller.process_form_data(dict(request.form), *required_keys)
    except (AttributeError, ValueError):
        error = "Invalid form input"
    
    if form_data:
        try:
            user = db.get_user_by_email(form_data['email'])
            if user is None:
                raise KeyError('User non-existent')
        except KeyError:
            error = "User does not exist"
        else:
            # if user exists, check against the saved password
            if user.password == form_data['password']:
                # if it is the same, save username to session
                controller.add_user_to_session(user.key)
                flash('Login successful')
                return redirect(url_for('categories_list',
                                user_key=user.key))
            else:
                error = "Invalid password or username"
    if error:
        flash(error)
    return redirect(url_for('index'))


@app.route('/user/v<int:user_key>/categories', methods=['GET', 'POST'])
def categories_list(user_key):


    return render_template('home.html')


# 

if __name__ == '__main__':
    app.run()