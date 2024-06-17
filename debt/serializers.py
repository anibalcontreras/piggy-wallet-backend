from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Debt


class DebtSerializer(serializers.ModelSerializer):
    user = UserSerializer(readonly=True)
    debtor = UserSerializer(readonly=True)

    class Meta:
        model = Debt
        fields = "__all__"
