from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, mixins, GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import Country, State, City
from location.serializer import CountrySerializer, StateSerializer, StateListSerializer, CitySerializer, CityListSerializer


class CountryListViewSet(ModelViewSet):
    """
    view set from list and retrieve countries
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_permissions(self):
        """"""
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method == "PUT" or self.request.method == 'POST' or self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
        return [auth() for auth in self.authentication_classes]


class StateViewSet(ModelViewSet):
    """
    view set from list and retrieve states
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get_permissions(self):
        """"""
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def get_authenticators(self):
        if self.request.method == "PUT" or self.request.method == 'POST' or self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
        return [auth() for auth in self.authentication_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StateListSerializer
        return self.serializer_class


class CityViewSet(ModelViewSet):
    """
    view set from list and retrieve cities
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        """"""
        if self.action == 'update' or self.action == 'create' or self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def get_authenticators(self):
        if self.request.method == "PUT" or self.request.method == 'POST' or self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
        return [auth() for auth in self.authentication_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CityListSerializer
        return self.serializer_class
