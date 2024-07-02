from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Expense
from user_expense_type.models import UserExpenseType
from categories.models import Category
from bankcard.models import BankCard


class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.UUIDField()
    user_expense_type = serializers.PrimaryKeyRelatedField(queryset=UserExpenseType.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    bankcard_id = serializers.PrimaryKeyRelatedField(queryset=BankCard.objects.all())
    amount = serializers.IntegerField()
    description = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        user_expense_type = data.get("user_expense_type")
        username = data.get("username")
        if (
            user_expense_type
            and not UserExpenseType.objects.filter(id=user_expense_type.id, username=username).exists()
        ):
            raise serializers.ValidationError(
                {"user_expense_type": "This user_expense_type does not belong to the specified user."}
            )

        return data

    def create(self, validated_data):
        user_id = validated_data.get("username")
        if "user_expense_type" not in validated_data:
            default_expense_type = UserExpenseType.objects.filter(
                username=user_id, name="Personal", set_by_user=False
            ).first()
            if not default_expense_type:
                raise serializers.ValidationError("Default personal expense type not found for the user.")
            validated_data["user_expense_type"] = default_expense_type

        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.description = validated_data.get("description", instance.description)
        instance.bankcard_id = validated_data.get("bankcard_id", instance.bankcard_id)
        instance.user_expense_type = validated_data.get("user_expense_type", instance.user_expense_type)
        instance.category = validated_data.get("category", instance.category)
        instance.save()
        return instance
