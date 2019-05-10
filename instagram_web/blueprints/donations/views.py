from flask import Flask, Blueprint, redirect, url_for, render_template, request, flash
import braintree
from instagram_web.util.braintree import generate_client_token, transact, find_transaction
from models.image import Image


donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


# @donations_blueprint.route("/client_token", methods=["GET"])
# def client_token():
#   return generate_client_token()


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


@donations_blueprint.route('/<id>/new', methods=['GET'])
def new_donation(id):
    image = Image.get_by_id(id)
    client_token = generate_client_token()
    return render_template('donations/new.html', image=image, client_token=client_token)

@donations_blueprint.route('<id>/<transaction_id>', methods=['GET'])
def show_checkout(id, transaction_id):
    image = Image.get_by_id(id)
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your text transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }
    
    return render_template('donations/show.html', transaction=transaction, result=result, username=image.user.username)

@donations_blueprint.route('/<id>/donations', methods=['POST'])
def create_checkout(id):
    image = Image.get_by_id(id)
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        # return redirect(url_for('users.show', username=image.user.username))
        return redirect(url_for('donations.show_checkout', transaction_id=result.transaction.id, id=image))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.show', username=image.user.username))