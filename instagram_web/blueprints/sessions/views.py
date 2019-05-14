from flask import Flask, session, Blueprint,redirect, render_template
import os
from werkzeug.security import check_password_hash
from app import login_manager
from flask import request, flash, url_for
from models.user import User
from flask_login import login_user, current_user, logout_user
from instagram_web.helpers.google_oauth import oauth


@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
    # The above is not applicable for peewee
    # We need to let login_manger knows how to retrieve User
    return User.get_by_id(user_id)

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates/sessions')




@sessions_blueprint.route('/new', methods=['GET'])
def new():
        return render_template('new.html')

@sessions_blueprint.route('/login', methods=['POST'])
def create():
        if current_user.is_authenticated:
                flash('Logged', 'warning')
        
        # Checks if USERNAME exists in database
        given_username = request.form['user_name']
        username_check = User.get_or_none(User.username == given_username)
        if not username_check:
                flash(f"User doesn't exist yo.")
                return render_template('new.html', title="Sign In")
        
        # Checks if EMAIL exists in database
        email = request.form['email']
        email_check = User.get_or_none(User.email == email)
        if not email_check:
                flash(f"Email doesn't exist yo.")
                return render_template('new.html', title="Sign In")

        # Check is email and username belong to same user account
        double_check = ((username_check.email == email_check.email) and (username_check.username == email_check.username))
        if not double_check:
                flash('This username and email combination does not match!')
                return render_template('new.html', title="Sign In")

        # Check if PASSWORD is correct and matches with hashed one
        user = User.get_or_none(User.email == email)
        password_to_check = request.form['password']

        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        
        if not result:
                flash(f"Invalid password")
                return render_template('new.html', title="Sign In") 

        if username_check and email_check and result:
                flash(f'Welcome back {user.username}!', 'success')
                if request.form.get('remember_me'):
                        flash('REMEMBERED!')
                        login_user(user, remember=True) #flask-login sets user_id in session
                else:
                        login_user(user)
                        return redirect(url_for('users.show', username=user.username))

        else:
                flash('Invalid login credentials', 'danger')
                return render_template('new.html', title="Sign In")

@sessions_blueprint.route('logout')
def logout():
        logout_user()
        flash(f'You were logged out.', 'warning')
        return redirect(url_for('home'))



@sessions_blueprint.route('google_login/authorize', methods=["GET"])
def authorize():
        token = oauth.google.authorize_access_token()

        if token:
                email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
                user = User.get_or_none(User.email == email)

                if not user:
                        flash('Not registered with Google', 'danger')
                        return redirect(url_for('users.show', username=user.username))
                
                else:
                        login_user(user)
                        flash(f'Welcome back {{user.username}}')
                        return redirect(url_for('users.show', username=user.username))
                # return redirect(url_for('users.show', username=user.username))
        else:
                flash('User not found', 'danger')
                return redirect(url_for('users.show', username=user.username))
                
               

@sessions_blueprint.route('google_login', methods=['GET'])
def google_login():
        redirect_uri = url_for('sessions.authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)