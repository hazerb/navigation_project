from rest_framework import serializers
from navigationApp.models import NavigationRecord, Vehicle

class NavigationRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = NavigationRecord
		fields = ('id', 'vehicle', 'datetime', 'latitude', 'longitude')
		
class VehicleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vehicle
		fields = ('id', 'plate')

class NavigVehicleSerializer(serializers.ModelSerializer):
	vehicle_plate = serializers.CharField(source='vehicle.plate')
	class Meta:
		model = NavigationRecord
		fields = ('latitude', 'longitude', 'vehicle_plate', 'datetime')
