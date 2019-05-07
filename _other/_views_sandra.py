@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    # use User.validate_password to call the function if it's got a @classmethod. Otherwise, do newuser.validate_password to call the function

    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('users/new.html')

    newuser = User(
        username=user_name,
        email=email,
        password=hashed_password
    )

    if newuser.save():
        flash(f'Welcome {user_name}')
        return redirect(url_for('users.new'))

    else:
        flash(f'{user_name} is already taken. Pick another')
        return render_template('users/new.html', errors=newuser.errors)