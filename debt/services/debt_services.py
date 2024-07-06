from debt.models import Debt
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

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
    debts = Debt.objects.filter(user=user).filter(is_paid=False) | Debt.objects.filter(debtor=user).filter(
        is_paid=False
    )

    users = set()
    for debt in debts:
        if debt.user != user:
            users.add(debt.user)
        if debt.debtor != user:
            users.add(debt.debtor)

    return users


def settle_debts(user_id, other_user_id):
    user = User.objects.get(user_id=user_id)
    other_user = User.objects.get(user_id=other_user_id)

    debts_as_user = Debt.objects.filter(user=user, debtor=other_user, is_paid=False)
    debts_as_debtor = Debt.objects.filter(user=other_user, debtor=user, is_paid=False)

    debts_as_user.update(is_paid=True)
    debts_as_debtor.update(is_paid=True)


def toggle_debt_payment(debt_id):
    try:
        debt = Debt.objects.get(id=debt_id)
        debt.is_paid = not debt.is_paid
        debt.save()
        return debt
    except Debt.DoesNotExist:
        raise ValueError("Debt not found")


def get_unpaid_debts_by_week(user_id, other_user_id):
    now = timezone.now()
    start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_last_week = start_of_week - timedelta(weeks=1)

    present_week_debts = Debt.objects.filter(
        (
            Q(user__user_id=user_id) & Q(debtor__user_id=other_user_id)
            | Q(user__user_id=other_user_id) & Q(debtor__user_id=user_id)
        ),
        is_paid=False,
        created_at__gte=start_of_week,
    )

    last_week_debts = Debt.objects.filter(
        (
            Q(user__user_id=user_id) & Q(debtor__user_id=other_user_id)
            | Q(user__user_id=other_user_id) & Q(debtor__user_id=user_id)
        ),
        is_paid=False,
        created_at__gte=start_of_last_week,
        created_at__lt=start_of_week,
    )

    previous_debts = Debt.objects.filter(
        (
            Q(user__user_id=user_id) & Q(debtor__user_id=other_user_id)
            | Q(user__user_id=other_user_id) & Q(debtor__user_id=user_id)
        ),
        is_paid=False,
        created_at__lt=start_of_last_week,
    )

    return present_week_debts, last_week_debts, previous_debts
