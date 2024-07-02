from rest_framework import serializers
from .models import BankCard


class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = "__all__"

    def create(self, validated_data):
        return BankCard.objects.create(**validated_data)
