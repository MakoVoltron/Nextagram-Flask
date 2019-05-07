from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash

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



# @users_blueprint.route('/login', methods=['GET'])
# def login():
#     render_template('users/login.html', title="Sign In")
#     password_to_check = request.form['password']
#     hashed_password = user.hashed_password
#     result = check_password_hash(hashed_password, password_to_check)

#     if result == True:
#         flash('Welcome back {user.username}!', 'success')
#     else:
#         flash('Invalid login credentials', 'danger')

    # return render_template('users/login.html', title="Sign In")




@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_by_id(username)
    return render_template('show.html')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass




# @users_blueprint.route('/', methods=['GET'])
# def login():
#     user = User.get_by_id(username)
#     return render_template('show.html')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     breakpoint()
#     if form.validate_on_submit():
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     else:
#         # flash(f'Account Error', 'danger')
#         return render_template('register.html', title="Sign Up", form=form)

# REDUNTANT? - DELETE? 
# @users_blueprint.route('/', methods=['POST'])
# def signup():
#     pass
# REDUNTANT? - DELETE? 
  