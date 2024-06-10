from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.UUIDField()
    expense_type_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    bankcard_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
