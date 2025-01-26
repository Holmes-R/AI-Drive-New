from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital
from .models import Blood, Cylinder, Organ, Availability, Hospital
from django.shortcuts import render, redirect ,get_list_or_404 , get_object_or_404
from django.views.generic.edit import FormView
from .serializer import *
from .forms import AppointmentForm 
from django.http import JsonResponse



from django.views import View

def home(request):
    return render(request, 'home.html')
class HospitalListCreateView(APIView):
  
    def get(self, request, *args, **kwargs):

        hospitals = Hospital.objects.all()
        serialized_data = [
            {
                "HospitalName": hospital.HospitalName,
                "Admin": hospital.Admin,
                "Address": hospital.Address,
                "Pincode": hospital.Pincode,
                "PhoneNumber": hospital.PhoneNumber,
                "AvailableDoctors": hospital.AvailableDoctors,
            }
            for hospital in hospitals
        ]
        return render(request, 'hospital_list.html', {'hospitals': serialized_data})


    def post(self, request, *args, **kwargs):
        serializer = HospitalSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class HospitalSearchView(View):
    def get(self, request):
        query = request.GET.get('search', '')
        hospitals = Hospital.objects.filter(HospitalName__icontains=query)
        return render(request, 'hospital_list.html', {'hospitals': hospitals})
class HospitalDetailView(APIView):


    def get(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(HospitalName=hospital_name)
            
            doctors = hospital.Doctors.all()  
            availability = hospital.availabilities.all()  
            blood_types = hospital.blood_types.all()  
            organs = hospital.organs.all()
            
            context = {
                'hospital': hospital,
                'doctors': doctors,
                'availability': availability,
                'blood_types': blood_types,
                'organs': organs,
            }
            return render(request, 'hospital_detail.html', context)

        except Hospital.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)


class AppointmentCreateView(FormView):
    template_name = 'appointment_form.html'
    form_class = AppointmentForm 
    success_url = '/appointment_success/'  

    def form_valid(self, form):
        form.save() 
        return redirect('appointment_success') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospitals'] = Hospital.objects.all() 
        return context
    

def request_resource(request):
    if request.method == "POST":
        resource_type = request.POST.get("resource_type")
        quantity = int(request.POST.get("quantity"))
        hospital_id = request.POST.get("hospital_id")

        hospital = get_object_or_404(Hospital, id=hospital_id)

        if resource_type == "blood":
            blood_type = request.POST.get("blood_type")
            if not blood_type:
                return JsonResponse({"error": "Blood type is required."}, status=400)

            blood = hospital.blood_types.filter(BloodType=blood_type).first()
            if blood and blood.Qantity >= quantity:
                blood.Qantity -= quantity
                blood.save()
                # Send updated blood types in the response
                updated_blood_types = [
                    f"{b.BloodType} ({b.Qantity} units)" for b in hospital.blood_types.all()
                ]
                return JsonResponse({
                    "message": f"Successfully requested {quantity} units of {blood_type} blood.",
                    "updated_resources": {
                        "blood_types": updated_blood_types,
                    }
                })
            else:
                return JsonResponse({"error": f"Not enough {blood_type} blood available."}, status=400)

        elif resource_type == "cylinder":
            cylinder_type = request.POST.get("cylinder_type")
            cylinder = hospital.cylinders.filter(CylinderType=cylinder_type).first()

            if cylinder and cylinder.Quantity >= quantity:
                cylinder.Quantity -= quantity
                cylinder.save()
                return JsonResponse({"message": f"Successfully requested {quantity} {cylinder_type} cylinders."})
            else:
                return JsonResponse({"error": f"Not enough {cylinder_type} cylinders available."}, status=400)

        elif resource_type == "organ":
                organ_type = request.POST.get("organ_type")
                quantity = request.POST.get("quantity")

                if not organ_type or not quantity:
                    return JsonResponse({"error": "Organ type and quantity are required."}, status=400)

                # Ensure quantity is a valid integer
                try:
                    quantity = int(quantity)
                except ValueError:
                    return JsonResponse({"error": "Invalid quantity."}, status=400)

                organ = hospital.organs.filter(OrganAvailable=organ_type).first()

                if organ:
                    # Decrease the available organs by the requested quantity
                    if organ.Quantity >= quantity:
                        organ.Quantity -= quantity
                        organ.save()
                        # Send updated organ details in the response
                        updated_organs = [o.OrganAvailable for o in hospital.organs.all()]
                        return JsonResponse({
                            "message": f"Successfully requested {quantity} {organ_type} organs.",
                            "updated_resources": {
                                "organs": updated_organs,
                            }
                        })
                    else:
                        return JsonResponse({"error": f"Not enough {organ_type} organs available."}, status=400)
                else:
                    return JsonResponse({"error": f"{organ_type} organ not available."}, status=400)


        elif resource_type == "ambulance":
            availability = hospital.availabilities.first()
            if availability and availability.Ambulance_count >= quantity:
                availability.Ambulance_count -= quantity
                availability.save()
                return JsonResponse({"message": f"Successfully requested {quantity} ambulances."})
            else:
                return JsonResponse({"error": f"Not enough ambulances available."}, status=400)

        else:
            return JsonResponse({"error": "Invalid resource type."}, status=400)

    return render(request, "request_resource.html", {"hospitals": Hospital.objects.all()})


def get_hospital_resources(request, hospital_name):
    hospital = get_object_or_404(Hospital, HospitalName__iexact=hospital_name)

    resources = {
        "blood_types": [f"{b.BloodType} ({b.Qantity} units)" for b in hospital.blood_types.all()],
        "cylinders": [f"{c.CylinderType} ({c.Quantity} units)" for c in hospital.cylinders.all()],
        "organs": [o.OrganAvailable for o in hospital.organs.all()],
        "ambulances": hospital.availabilities.first().Ambulance_count if hospital.availabilities.exists() else 0,
    }

    return JsonResponse(resources)