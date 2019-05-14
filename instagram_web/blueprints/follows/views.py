from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from models.user import User
from models.followerfollowing import FollowerFollowing
from flask_login import current_user

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/<idol_id>', methods=['POST'])
@login_required     # if using this decorator....
def create(idol_id):
    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash('No user found with this i!', 'warning')
        return redirect(url_for('home'))
    
    # if not current_user.is_authenticated:       # ...we don't need this code, because it's handled by dcorator @login_required
    #     flash('Please, login to continue', 'warning')
    #     return redirect(url_for('sessions.new'))

    new_follow = FollowerFollowing(
        fan_id = current_user.id,
        idol_id = idol.id
    )

    if not idol.is_private:
        new_follow.approved = True

    for i in current_user.idols:
        if i.idol_id == idol.id:
            flash('You already follow that dude!', 'warning')
            return redirect(url_for('users.show', username=idol.username))

    if not new_follow.save():
        flash('Unable to follow this user!', 'danger')
        return redirect(url_for('users.show', username=idol.username))


    if new_follow.is_approved:
        flash(f'You are now following {idol.username}', 'success')
        return redirect(url_for('users.show', username=idol.username))

    flash('Follow request sent! Please, wait for pproval', 'success')
    return redirect(url_for('users.show', username=idol.username))


@follows_blueprint.route('/<idol_id>/delete', methods=['POST'])
@login_required
def delete(idol_id):
    idol = User.get_or_none(User.id == idol_id)


    unfollow = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == idol_id) & (FollowerFollowing.fan_id == current_user.id))

    if not unfollow.delete_instance():
        flash(f'Unable to unfollow {idol.username}', 'warning')
        return redirect(url_for('users.show', username=idol.username))

    flash(f'You unfollowed {idol.username}', 'warning')
    return redirect(url_for('users.show', username=idol.username))
