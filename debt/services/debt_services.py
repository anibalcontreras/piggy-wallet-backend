from debt.models import Debt
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_debts(user):
    return Debt.objects.filter(user=user) | Debt.objects.filter(debtor=user)


def calculate_balance(user_id, other_user_id):
    user = User.objects.get(user_id=user_id)
    other_user = User.objects.get(user_id=other_user_id)

    debts_as_user = Debt.objects.filter(user=user, debtor=other_user, is_paid=False)
    debts_as_debtor = Debt.objects.filter(user=other_user, debtor=user, is_paid=False)

    balance = 0
    for debt in debts_as_user:
        balance += debt.amount

    for debt in debts_as_debtor:
        balance -= debt.amount

    return balance


def get_related_users(user_id):
    user = User.objects.get(user_id=user_id)
    debts = Debt.objects.filter(user=user) | Debt.objects.filter(debtor=user)

    users = set()
    for debt in debts:
        if debt.user != user:
            users.add(debt.user)
        if debt.debtor != user:
            users.add(debt.debtor)

    return users
