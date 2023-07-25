from rest_framework import serializers
from core.models import Country, State, City


class CountrySerializer(serializers.ModelSerializer):
    """ Model serializer from Country model """

    class Meta:
        model = Country
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)


class StateSerializer(serializers.ModelSerializer):
    """ Model serializer from state model """
    class Meta:
        model = State
        fields = ('id', 'name', 'code', 'country')
        read_only_fields = ('id',)


class StateListSerializer(StateSerializer):
    class Meta(StateSerializer.Meta):
        depth = 1


class CitySerializer(serializers.ModelSerializer):
    """ Model serializer from city model """
    class Meta:
        model = City
        fields = ('id', 'name', 'code', 'state')
        read_only_fields = ('id',)


class CityListSerializer(CitySerializer):
    class Meta(CitySerializer.Meta):
        depth = 1
