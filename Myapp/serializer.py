from rest_framework import serializers
from .models import *

class BloodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood
        fields = "__all__"

class CylinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cylinder
        fields = "__all__"

class OrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    hospital = serializers.StringRelatedField() 

    class Meta:
        model = Doctor
        fields = ['DoctorName', 'Doc_PhoneNumber', 'hospital', 'Specialization']

class AvailabilitySerializer(serializers.ModelSerializer):
    hospital = serializers.StringRelatedField()  

    class Meta:
        model = Availability
        fields = ['id', 'Ambulance_count', 'hospital']

class AppointmentSerializer(serializers.ModelSerializer):
    HospitalName = serializers.StringRelatedField()  

    class Meta:
        model = Appointment
        fields = ['id', 'PatientName', 'Age', 'Description', 'HospitalName', 'date']

class HospitalSerializer(serializers.Serializer):
    blood_types = BloodSerializer(many=True, read_only=True)
    cylinders = CylinderSerializer(many=True, read_only=True)
    organs = OrganSerializer(many=True, read_only=True)
    Doctors = DoctorSerializer(many=True, read_only=True)
    availabilities = AvailabilitySerializer(many=True, read_only=True)
    Appointments = AppointmentSerializer(many=True, read_only=True)
    class Meta:
        models = Hospital
        fields = "__all__"
        exclude = ['Is_Active']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['PatientName', 'Age', 'Description', 'HospitalName', 'date']