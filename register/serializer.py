from rest_framework import serializers
from core.models import Citizen


class CitizenSerializer(serializers.ModelSerializer):
    """ Model serializer from city model """

    def validate_phone(self, value):
        if len(str(value)) > 10:
            raise serializers.ValidationError("Ensure this field has no more than 10 characters")
        return value

    def validate_no_identification(self, value):
        if len(str(value)) > 10:
            raise serializers.ValidationError("Ensure this field has no more than 10 characters")
        return value

    class Meta:
        model = Citizen
        fields = ('id', 'name', 'last_name', 'address', 'phone', 'no_identification', 'city')
        read_only_fields = ('id',)


class CitizenListSerializer(CitizenSerializer):
    class Meta(CitizenSerializer.Meta):
        depth = 1
