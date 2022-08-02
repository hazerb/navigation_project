from django.db import models

# Create your models here.


class NavigationRecord(models.Model):
	id = models.AutoField(primary_key=True)
	vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	latitude = models.FloatField()
	longitude = models.FloatField()
	
	
class Vehicle(models.Model):
	id = models.AutoField(primary_key=True)
	plate = models.CharField(max_length=500)
	
