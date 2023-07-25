from django.urls import path, include
from rest_framework.routers import DefaultRouter
from location.views import CountryListViewSet, StateViewSet, CityViewSet

router = DefaultRouter()
router.register('countries', CountryListViewSet, basename='country')
router.register('states', StateViewSet, basename='state')
router.register('cities', CityViewSet, basename='city')

app_name = 'location'

urlpatterns = [
    path('', include(router.urls))
]
