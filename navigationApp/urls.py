from django.conf.urls import url
from navigationApp import views


urlpatterns = [
	url(r'get_data', views.get_records),
	url(r'seed', views.seed),
	url(r'add_record', views.add_record),
]
