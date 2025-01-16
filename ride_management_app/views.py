from rest_framework import viewsets, permissions, filters
from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer # type: ignore
from django.utils.timezone import now, timedelta
from django.db.models import Prefetch

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.prefetch_related(
        Prefetch('events', queryset=RideEvent.objects.filter(created_at__gte=now() - timedelta(days=1)))
    ).select_related('id_rider', 'id_driver')
    serializer_class = RideSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['id_rider__email']
    ordering_fields = ['pickup_time', 'pickup_latitude', 'pickup_longitude']

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
