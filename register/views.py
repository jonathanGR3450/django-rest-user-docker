from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from register.serializer import CitizenSerializer, CitizenListSerializer
from core.models import Citizen
from register.permissions import CitizensOwnerUser


class CitizenModelViewSet(ModelViewSet):
    """ model view set citizen model """
    permission_classes = [IsAuthenticated, CitizensOwnerUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = CitizenSerializer

    def perform_create(self, serializer):
        """ save user auth """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CitizenListSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'list':
            return Citizen.objects.filter(user=self.request.user)
        return Citizen.objects.all()
