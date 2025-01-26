from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Blood)
admin.site.register(Cylinder)
admin.site.register(Availability)
admin.site.register(Organ)
admin.site.register(Appointment)