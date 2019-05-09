from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import current_user
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html', title="Sign Up")


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not password == confirm_password:
        flash('Passwords do not match!', 'warning')
        return render_template('users/new.html')
    hashed_password = generate_password_hash(password)

    # use User.validate_password to call the function if it's 
    # got a @classmethod. Otherwise, do newuser.validate_password 
    # to call the function
    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('users/new.html')

    newuser = User(
        username=user_name,
        email=email,
        password=hashed_password
    )

    if newuser.save():
        flash(f"Your account has been created, {user_name}! Proceed to login.")
        return redirect(url_for('sessions.new'))

    else:
        flash(f'{user_name} is already taken. Pick another.')
        return render_template('users/new.html', errors=newuser.errors)



# SHOW USER ACCOUNT
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username==username)
    if user.username == current_user.username:
        return render_template('users/show.html', user=user)
    else:
        return render_template('users/users.html', user=user)

# @users_blueprint.route('/{{ current_user }}', methods=["GET"])
# def profile(username):
#     user = User.get(username=username)
#     return render_template('users/show.html', user=user)



# @users_blueprint.route('/<username>', methods=["GET"])
# def show(username):
#     user = User.get(username=username)
#     return render_template('users/show.html', user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    id = user.id
    
    if current_user == user:
        return render_template('users/edit.html', user=user)
    else:
        flash('Not authorised')
        return redirect(url_for('home'))

# UPDATE USER DETAILS
@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    if not current_user == user:
        flash('Not authorised')
        return redirect(url_for('users/edit.html', username=current_user.username))
    else:
        new_user_name = request.form.get('new_user_name')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')

        # VALIDATION CHECKS 
        
        # Checks if USERNAME exists in database
        username_check = User.get_or_none(User.username == new_user_name)
        if not username_check == user:
            if username_check and not username_check == user:
                    flash(f"User name is taken!", 'danger')
                    # return redirect(url_for('users.edit.html'))
                    return render_template('users/edit.html', user=user)
        
        # Checks if EMAIL exists in database
        email_check = User.get_or_none(User.email == new_email)
        if not email_check == user:
            if email_check:
                    flash(f"Email is taken! Try different one", 'danger')
                    return render_template('users/edit.html', user=user)


    # use UPDATE because using save will execute the validation in users.py
        update_user = User.update(
            username=new_user_name,
            email=new_email,
            password=new_password
        ).where(User.id == id)

        if not update_user.execute():
            flash(f'Unable to update, try again.', 'danger')
            return render_template('users/show.html')
        
        flash('Successfully updated', 'success')
        # return redirect(url_for('home'))
        return redirect(url_for('users.show'), username=new_user_name)

        

    
