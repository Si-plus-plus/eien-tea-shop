from .models import Transaction, Payment


def get_or_set_session(request):
    transaction_id = request.session.get('transaction_id', None)

    make_new_session = False

    try:
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.finished:
            make_new_session = True

    except Transaction.DoesNotExist:
        make_new_session = True

    if make_new_session:
        transaction = Transaction()
        transaction.save()
        request.session['transaction_id'] = transaction.id

    if request.user.is_authenticated and transaction.user is None:
        transaction.user = request.user
        transaction.save()
    return transaction
