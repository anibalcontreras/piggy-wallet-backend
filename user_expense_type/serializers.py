from rest_framework import serializers
from .models import UserExpenseType


class UserExpenseTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserExpenseType
        fields = ["id", "username", "name", "description", "set_by_user"]

    def create(self, validated_data):
        validated_data["set_by_user"] = True
        return UserExpenseType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
