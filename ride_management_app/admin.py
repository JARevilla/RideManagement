from django.contrib import admin
from .models import User, Ride, RideEvent
# Register your models here.

admin.site.register(User)
admin.site.register(Ride)
admin.site.register(RideEvent)
