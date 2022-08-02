from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache

from navigationApp.models import NavigationRecord, Vehicle
from navigationApp.serializers import NavigationRecordSerializer, VehicleSerializer, NavigVehicleSerializer

from datetime import datetime, timedelta
import random
import string
import json

@csrf_exempt
#this function gets in the last 48 hour records of each vehicle
def get_records(request):
	if request.method == 'GET':
		thetime = timezone.now() - timedelta(hours=48)
		#if new record was added after previous query then it's needed to make new query
		if cache.get("new_record"):
			vehicle_last_48_records = {}		#dictionary for storing navigation records of vehicles
			#inner join navigationrecord and vehicle tables and get result
			data = NavigationRecord.objects.filter(datetime__gte=thetime).select_related('vehicle')
			most_recent = []			#array for most recent navigation datas of each vehicle
			for record in data:
				plate = record.vehicle.plate
				#update navigation record of vehicle if it's more recent
				if plate not in vehicle_last_48_records or record.datetime > vehicle_last_48_records[plate].datetime:
					vehicle_last_48_records[plate] = record
			#append most recent data of each vehicle to most_recent
			for plate in vehicle_last_48_records:
				most_recent.append(vehicle_last_48_records[plate])
			data = most_recent
		#if there is no new record then simply return result in cache
		else:
			will_be_deleted = set()
			vehicle_last_48_records = cache.get('records')
			data = []
			#if navigation record is old then delete it from cache
			for record_plate in vehicle_last_48_records:
				if vehicle_last_48_records[record_plate].datetime < thetime:
					will_be_deleted.add(record_plate)
				else:
					data.append(vehicle_last_48_records[record_plate])
			for r in will_be_deleted:
				del vehicle_last_48_records[r]
		#put result in cache for later use
		cache.set("records", vehicle_last_48_records, 1000)
		nav_vehicle_serializer = NavigVehicleSerializer(data, many=True)
		cache.set("new_record", False)
		return JsonResponse(nav_vehicle_serializer.data, safe=False)
	else:
		return JsonResponse("no post method", safe=False)


@csrf_exempt
#this function adds new navigation record to database
def add_record(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		vehicle_plate = body['vehicle_plate']
		latitude = body['latitude']
		longitude = body['longitude']
		vehicle_id = Vehicle.objects.filter(plate=body['vehicle_plate'])[0].id
		NavigationRecord.objects.create(vehicle_id=vehicle_id, datetime=timezone.now(), latitude=latitude, longitude=longitude)
		#new record is added to database, so set "new_record" to true
		cache.set("new_record", True)
		return JsonResponse('201', safe=False)
	else:
		return JsonResponse('no get method', safe=False)


@csrf_exempt
#this function initiates the database with random values
def seed(request):
	if request.method == "POST":
		cache.set("new_record", True)
		plates = []
		for i in range(10):
			random_plate = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
			plates.append(random_plate)
			vehicle = Vehicle(plate=random_plate)
			vehicle.save()
		for i in range(100):
			vehicle_id = random.randrange(1, len(plates)+1)
			latitude = vehicle_id * random.random()
			longitude = vehicle_id * random.random()
			NavigationRecord.objects.create(vehicle_id=vehicle_id, datetime=timezone.now(), latitude=latitude, longitude=longitude)
		return JsonResponse("201", safe=False)
	else:
		return JsonResponse("no get method", safe=False)

