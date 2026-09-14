from django.db import transaction
from accounts.models import Wallet, WalletTransaction
from core.models import Seminar

class SeminarPurchaseError(Exception):
    pass

@transaction.atomic
def participate_in_seminar(user, seminar):
    if seminar.participants.filter(pk=user.pk).exists():
        raise SeminarPurchaseError('You are already participating in this seminar.')
    if seminar.price == 0:
        seminar.participants.add(user)
        return
    wallet = Wallet.objects.select_for_update().get(user=user)
    if wallet.balance < seminar.price:
        raise SeminarPurchaseError('Your wallet balance is not enough.')
    
    wallet.balance -= seminar.price
    wallet.save(update_fields=['balance'])
    WalletTransaction.objects.create(wallet=wallet, transaction_type=WalletTransaction.TransactionType.SEMINAR_PAYMENT, amount=seminar.price, description=f'payment for seminar: {seminar.title}')
    seminar.participants.add(user)