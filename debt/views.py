from rest_framework import viewsets
from .serializers import DebtSerializer, UserDebtSerializer
from .models import Debt
from django.contrib.auth import get_user_model
from authentication.decorators import cognito_authenticated
from rest_framework.response import Response
from rest_framework import status
from .services.get_user_debts import get_user_debts
from rest_framework.decorators import action
from authentication.utils import get_user_id_from_token

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
        user = User.objects.get(user_id=user_id)
        debts = get_user_debts(user)

        users = set()
        for debt in debts:
            if debt.user != user:
                users.add(debt.user)
            if debt.debtor != user:
                users.add(debt.debtor)

        serialized_users = UserDebtSerializer(users, many=True)
        return Response(serialized_users.data)
