from django.contrib import admin
from django.urls import path ,include
from .views import HospitalListCreateView,HospitalDetailView,AppointmentCreateView,request_resource , get_hospital_resources
from django.views.generic import TemplateView
from .views import HospitalSearchView, HospitalDetailView
from Myapp import views


urlpatterns = [
     path('', views.home, name='home'),
    path('hospitals/', HospitalListCreateView.as_view(), name='hospital_list'), 
    path('hospitals/<str:hospital_name>/', HospitalDetailView.as_view(), name='hospital_detail'),
    path('create_appointment/', AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointment_success/', TemplateView.as_view(template_name="appointment_success.html"), name='appointment_success'),
    path('request/', request_resource, name='request_resource'),
    path('get_hospital_resources/<str:hospital_name>/', views.get_hospital_resources, name='get_hospital_resources'),
]
    