from django.db import models
from datetime import timedelta
from django.utils.timezone import now


class User(models.Model):
    
    ROLE_CHOICES = [
        ("ADMIN", 'Admin'),
        ("RIDER", 'Rider'),
        ("DRIVER", 'Driver'),
    ]

    id_user = models.AutoField(primary_key=True,null=False)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=False)
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=100,null=False)
    phone_number = models.CharField(max_length=15,null=False)

class Ride(models.Model):
    
    STATUS_CHOICES = [
        ("PENDING", 'Pending'),
        ("EN_ROUTE", 'En-route'),
        ("PICKUP", 'Pickup'),
        ("DROPOFF", 'Dropoff')
    ]
        
    id_ride = models.AutoField(primary_key=True,null=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
        blank=False, 
        null=False
    )
    id_rider = models.ForeignKey(User, related_name='rides_as_rider', on_delete=models.CASCADE,null=False)
    id_driver = models.ForeignKey(User, related_name='rides_as_driver', on_delete=models.CASCADE,null=False)
    pickup_latitude = models.FloatField(null=False)
    pickup_longitude = models.FloatField(null=False)
    dropoff_latitude = models.FloatField(null=False)
    dropoff_longitude = models.FloatField(null=False)
    pickup_time = models.DateTimeField(null=False)

    class Meta:
        indexes = [
            models.Index(fields=['pickup_time']),
            models.Index(fields=['pickup_latitude', 'pickup_longitude']),
        ]

    def get_todays_events(self):
        """Retrieve RideEvents for this ride that occurred in the last 24 hours."""
        return self.events.filter(created_at__gte=now() - timedelta(days=1))

class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True,null=False)
    id_ride = models.ForeignKey(Ride, related_name='events', on_delete=models.CASCADE,null=False)
    description = models.CharField(max_length=255,null=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]