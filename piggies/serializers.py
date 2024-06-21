from rest_framework import serializers
from .models import Piggies


class PiggiesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Piggies
        fields = "__all__"

    def create(self, validated_data):
        return Piggies.objects.create(**validated_data)
