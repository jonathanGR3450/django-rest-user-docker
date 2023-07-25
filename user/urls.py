from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListUser, LoginUser, UserMe, count_user

app_name = 'user'

router = DefaultRouter()
router.register('users', ListUser)

urlpatterns = [
    # path('list-user/', ListUser.as_view(), name='create'),
    path('', include(router.urls)),
    path('token/', LoginUser.as_view(), name='token'),
    path('me/', UserMe.as_view(), name='me'),
    path('count/', count_user, name='count')
]
