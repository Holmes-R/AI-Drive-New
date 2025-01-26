from django.db import models
import re
from django.core.exceptions import ValidationError

def pincode_validator(value):
    if not re.match(r'^\d{6}$',value):
        raise ValidationError('Pincode must be exactly 6 digits.')

class Blood(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('O+', 'O+'),
        ('AB+', 'AB+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('O-', 'O-'),
        ('AB-', 'AB-'),
    ]
    BloodType = models.CharField(max_length=3, choices=BLOOD_TYPES, default='A+')
    Qantity = models.IntegerField(help_text="Quantity of Blood available") # (Units or Liters)

    def __str__(self):
        return f"{self.BloodType} - {self.Qantity} units"
    
    class Meta:
        verbose_name_plural = 'Blood'
    

class Cylinder(models.Model):
    CylinderType = models.CharField(max_length=50, help_text="Type of Cylinder (e.g., Oxygen)")
    Quantity = models.IntegerField(help_text="Quantity of Cylinders available") 

    def __str__(self):
        return f"{self.CylinderType} - {self.Quantity} cylinders"
    
    class Meta:
        verbose_name_plural = 'Cylinder'

class Organ(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('O+', 'O+'),
        ('AB+', 'AB+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('O-', 'O-'),
        ('AB-', 'AB-'),
    ]
    GENDER = [
        ('Male','Male'),
        ('Female','Female'),
        
    ]
    STATUS =[
        ('Alive','Alive'),
        ('Dead','Dead'),
    ]
    DonatorName = models.CharField(max_length=50,null=False,blank=False)
    DonarBloodType = models.CharField(max_length=3,choices=BLOOD_TYPES, default='A+')
    Gender = models.CharField(max_length=7,choices=GENDER,default=" ")
    Status = models.CharField(max_length=6,choices=STATUS,default="")
    OrganAvailable = models.CharField(max_length=10,blank=False,default=" ")

    def __str__(self):
        return f"{self.DonatorName} - {self.Gender} -{self.Status}"
    
    class Meta:
        verbose_name_plural = 'Organ' 


class Hospital(models.Model):
    HospitalName = models.CharField(help_text="Hospital Name",null=False,blank=False,unique=True,max_length=50)
    Admin = models.CharField(help_text="Hospital Admin",null=False,blank=False,max_length=50)
    Address = models.TextField(help_text="Hospital Address",null=False,blank=False,unique=False,max_length=100)
    Pincode = models.CharField(max_length=6,validators=[pincode_validator])
    PhoneNumber = models.CharField(help_text="Hospital Number",blank=False,max_length=13)
    AvailableDoctors = models.IntegerField()
    Is_Active = models.BooleanField(default=True)

    blood_types = models.ManyToManyField(Blood, related_name="hospitals")
    cylinders = models.ManyToManyField(Cylinder, related_name="hospitals")
    organs = models.ManyToManyField(Organ,related_name="hospitals")

    def save(self,*awgs,**kwargs):
        if not self.PhoneNumber.startswith("+91"):
            self.PhoneNumber = "+91" + self.PhoneNumber.lstrip("0")
        
        super().save(*awgs,**kwargs)
    
    def __str__(self):
        return self.HospitalName + " " + self.Admin    
    
    class Meta:
        verbose_name_plural = 'Hospital'

class Doctor(models.Model):
    DoctorName =  models.CharField(help_text="Doctor Name",null=False,blank=False,unique=True,max_length=50)
    Doc_PhoneNumber =  models.CharField(help_text="Doctor Number",blank=False,max_length=13)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,related_name="Doctors")
    Specialization = models.CharField(null=False,blank=False,max_length=40)
    def save(self,*awgs,**kwargs):
        if not self.Doc_PhoneNumber.startswith("+91"):
            self.Doc_PhoneNumber = "+91" + self.Doc_PhoneNumber.lstrip("0")
        
        super().save(*awgs,**kwargs)

    def __str__(self):
        return self.hospital.HospitalName + " " + self.DoctorName 
    
    class Meta:
        verbose_name_plural = 'Doctor'
    

class Availability(models.Model):
    Ambulance_count = models.IntegerField(blank=True, null=True, help_text="Number of Ambulances available")
    hospital = models.ForeignKey(Hospital, related_name="availabilities", on_delete=models.CASCADE) 
    def __str__(self):
        return f"Availability at {self.hospital.HospitalName}"
    
    class Meta:
        verbose_name_plural = 'Availability'


class Appointment(models.Model):
    PatientName = models.CharField(help_text="Patient Name",max_length=50)
    Age =models.CharField(help_text="Patient Age",max_length=3)
    Description = models.TextField(help_text="Patient Description")
    HospitalName = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name="Appointments")
    date = models.DateField()

    class Meta:
        verbose_name_plural = 'Appointment'
    def __str__(self):
        return f"{self.HospitalName} -- {self.PatientName}"