from rest_framework.routers import DefaultRouter  # type: ignore
from .views import UserViewSet, RideViewSet, RideEventViewSet
from rest_framework.authtoken.views import obtain_auth_token  # type: ignore
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)
router.register(r'ride-events', RideEventViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
    path('', include(router.urls)), 
]