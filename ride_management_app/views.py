from rest_framework import viewsets, permissions, filters
from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer # type: ignore
from django.utils.timezone import now, timedelta
from django.db.models import Prefetch, F, FloatField
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from django.db.models.functions import Sqrt, Power
from .apiaccesspermission import IsAPIAdminUser # type: ignore


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.prefetch_related(
        Prefetch(
            'events',
            queryset=RideEvent.objects.filter(created_at__gte=now() - timedelta(days=1)),
            to_attr='todays_ride_events'
        )
    ).select_related('id_rider', 'id_driver')
    serializer_class = RideSerializer
    permission_classes = [IsAPIAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by')
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if sort_by == 'distance' and latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
            except ValueError:
                return queryset.none()

            # Use the Haversine approximation for sorting by distance
            queryset = queryset.annotate(
                distance=Sqrt(
                    Power(F('pickup_latitude') - lat, 2) +
                    Power(F('pickup_longitude') - lon, 2)
                )
            ).order_by('distance')
        elif sort_by == 'pickup_time':
            queryset = queryset.order_by('pickup_time')
        return queryset

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
