@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    if not current_user == user:
        flash('You are not authorized to do this!')
        return render_template('edit_user.html', user=user)

    else:
        new_user_name = request.form.get('new_user_name')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')

    # use update because using save will execute the validation in users.py
        update_user = User.update(
            username=new_user_name,
            email=new_email,
            password=new_password
        ).where(User.id == id)

        if not update_user.execute():
            flash(
                f'Unable to update, please try again')
            return render_template('edit_user.html', user=user)

        flash('Successfully updated')
        return redirect(url_for('home'))