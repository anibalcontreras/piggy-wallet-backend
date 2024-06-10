from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.Serializer):
    username = serializers.UUIDField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        return Budget.objects.create(**validated_data)
