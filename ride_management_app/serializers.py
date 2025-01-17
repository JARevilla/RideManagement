from rest_framework import serializers
from .models import User, Ride, RideEvent

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    events = RideEventSerializer(many=True, read_only=True)
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    distance = serializers.FloatField(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = '__all__'
    
    def get_todays_ride_events(self, obj):
        return RideEventSerializer(obj.todays_ride_events, many=True).data
