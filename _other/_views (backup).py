from flask import Blueprint, render_template


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    # return render_template('users/new.html')
    return render_template('signup.html', title="Sign Up")


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

@users_blueprint.route('/', methods=['POST'])
def signup():
  
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
