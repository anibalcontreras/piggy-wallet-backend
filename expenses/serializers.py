from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Expense
from user_expense_type.models import UserExpenseType
from categories.models import Category
from bankcard.models import BankCard


class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    user_expense_type = serializers.PrimaryKeyRelatedField(queryset=UserExpenseType.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    bankcard_id = serializers.PrimaryKeyRelatedField(queryset=BankCard.objects.all())
    amount = serializers.IntegerField()

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
