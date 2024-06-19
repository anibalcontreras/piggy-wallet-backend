from rest_framework import viewsets
from .serializers import DebtSerializer, UserDebtSerializer
from .models import Debt
from django.contrib.auth import get_user_model
from authentication.decorators import cognito_authenticated
from rest_framework.response import Response
from rest_framework import status
from .services.debt_services import get_user_debts
from rest_framework.decorators import action
from authentication.utils import get_user_id_from_token
from .services.debt_services import get_related_users, calculate_balance, settle_debts, toggle_debt_payment

User = get_user_model()


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

    def get_queryset(self):
        user_id = get_user_id_from_token(self.request)
        user = User.objects.get(user_id=user_id)
        return get_user_debts(user)

    @cognito_authenticated
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            try:
                debtor = User.objects.get(user_id=self.request.data["debtor_id"])
                serializer.save(user=user, debtor=debtor)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error": "Debtor not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @cognito_authenticated
    @action(detail=False, methods=["get"])
    def users(self, request, *args, **kwargs):
        user_id = get_user_id_from_token(request)
        related_users = get_related_users(user_id)
        serialized_users = UserDebtSerializer(related_users, many=True)
        return Response(serialized_users.data)

    @cognito_authenticated
    @action(detail=False, methods=["get"], url_path="balance/(?P<other_user_id>[^/.]+)")
    def balance(self, request, other_user_id=None):
        user_id = get_user_id_from_token(request)
        balance = calculate_balance(user_id, other_user_id)
        result = {"balance": balance}
        return Response(result, status=status.HTTP_200_OK)

    @cognito_authenticated
    @action(detail=False, methods=["post"], url_path="settle/(?P<other_user_id>[^/.]+)")
    def settle(self, request, other_user_id=None):
        user_id = get_user_id_from_token(request)
        settle_debts(user_id, other_user_id)
        return Response({"status": "Debts settled"}, status=status.HTTP_200_OK)

    @cognito_authenticated
    @action(detail=False, methods=["put"], url_path="toggle-payment/(?P<debt_id>[^/.]+)")
    def toggle_payment(self, request, debt_id=None):
        try:
            debt = toggle_debt_payment(debt_id)
            return Response({"is_paid": debt.is_paid}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
