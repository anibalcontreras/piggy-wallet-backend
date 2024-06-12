from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.Serializer):
    username = serializers.UUIDField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        return Budget.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
