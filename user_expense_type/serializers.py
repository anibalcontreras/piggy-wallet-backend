from rest_framework import serializers
from .models import UserExpenseType


class UserExpenseTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserExpenseType
        fields = "__all__"

    # username = serializers.UUIDField()
    # name = serializers.CharField(max_length=70, default="Personal")
    # description = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    # set_by_user = serializers.BooleanField(default=False)
    # category_name = serializers.CharField(max_length=70)

    def create(self, validated_data):
        return UserExpenseType.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.set_by_user = validated_data.get("set_by_user", instance.set_by_user)
        instance.category_name = validated_data.get("category_name", instance.category_name)
        instance.save()
        return instance
