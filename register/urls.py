from django.urls import path, include
from rest_framework.routers import DefaultRouter
from register.views import CitizenModelViewSet

app_name = 'register'

router = DefaultRouter()
router.register('citizens', CitizenModelViewSet, basename='citizen')

urlpatterns = [
    path('', include(router.urls)),
]
