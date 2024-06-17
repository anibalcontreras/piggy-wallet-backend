from rest_framework import viewsets
from .serializers import DebtSerializer, Debt
from django.conf import settings
from django.contrib.auth import get_user_model
from authentication.decorators import cognito_authenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

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
