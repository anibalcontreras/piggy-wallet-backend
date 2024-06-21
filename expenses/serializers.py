from rest_framework import serializers
from .models import Expense
from user_expense_type.models import UserExpenseType
from categories.models import Category


class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.UUIDField()
    user_expense_type = serializers.PrimaryKeyRelatedField(queryset=UserExpenseType.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    bankcard_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
