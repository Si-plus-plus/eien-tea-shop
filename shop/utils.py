from .models import Transaction


def get_or_set_session(request):
    transaction_id = request.session.get('transaction_id', None)

    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = Transaction()
        transaction.save()
        request.session['transaction_id'] = transaction.id

    if request.user.is_authenticated and transaction.user is None:
        transaction.user = request.user
        transaction.save()
    return transaction


def get_or_set_transaction_session(request):
    transaction_id = request.session.get('transaction_id', None)

    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = Transaction()
        transaction.save()
        request.session['order_id'] = transaction.id

    if request.user.is_authenticated and transaction.user is None:
        transaction.user = request.user
        transaction.save()
    return transaction
