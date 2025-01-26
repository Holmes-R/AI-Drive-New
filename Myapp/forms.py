from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['PatientName', 'Age', 'Description', 'HospitalName', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  
        }
