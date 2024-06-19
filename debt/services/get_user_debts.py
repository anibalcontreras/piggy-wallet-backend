from debt.models import Debt


def get_user_debts(user):
    return Debt.objects.filter(user=user) | Debt.objects.filter(debtor=user)
