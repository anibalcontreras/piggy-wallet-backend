from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Debt


class DebtSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    debtor = UserSerializer(read_only=True)

    class Meta:
        model = Debt
        fields = "__all__"
        read_only_fields = ["user", "debtor"]


class UserDebtSerializer(serializers.Serializer):
    user_id = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
