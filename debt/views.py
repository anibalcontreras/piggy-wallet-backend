from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DebtSerializer, Debt
from django.contrib.auth.models import User


# Create your views here.
class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.Objects.all()
    serializer_class = DebtSerializer

    def perform_create(self, serializer):
        user = self.request.user
        debtor = User.objects.get(id=self.request.data["debtor_id"])
        serializer.save(user=user, debtor=debtor)
