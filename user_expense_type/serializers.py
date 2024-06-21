from rest_framework import serializers
from .models import UserExpenseType


class UserExpenseTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserExpenseType
        fields = "__all__"

    def create(self, validated_data):
        return UserExpenseType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.set_by_user = validated_data.get("set_by_user", instance.set_by_user)
        instance.save()
        return instance
