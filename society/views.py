from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.models import User as AuthUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Building, Societyprofile
from .forms import SocietyprofileForm, BuildingForm
from .serializers import SocietyProfileSerializer
from user.models import User,Society 


def home(request):
   return HttpResponse("Welcome to the Society Home Page")


import logging

logger = logging.getLogger(__name__)

def soc_profile(request,id):
    if request.user.is_superuser:
        society = get_object_or_404(Society, pk=id)
    elif request.user.is_admin:
        if id == request.user.id:
            society = request.user.society
        else:
            society = get_object_or_404(Society, pk=id)
    else:
        society = request.user.society
        if society.id != id:
            return HttpResponseForbidden("You don't have permission to access this society's profile.")
    
    logger.info(f"Retrieved Society: {society}")

    society_profile, created = Societyprofile.objects.get_or_create(society=society)
       
    if request.method == 'POST':
        form = SocietyprofileForm(request.POST, instance=society_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.society = society  
            profile.save()
            return redirect('id_soc_profile', id=society.id)
    else:
        initial_data = {
            'name_display': society.name if hasattr(society, 'name') else society,
            'society_type_display': ', '.join([str(t) for t in society.type.all()]) if hasattr(society, 'type') and society.type else ''
        }
        form = SocietyprofileForm(instance=society_profile, initial=initial_data)
        pass

    return render(request, 'society/soc_profile.html', {'socform': form})


def Societyprofile_admin_view(request):
    
       
    society_profile = get_object_or_404(Societyprofile, name_name=request.user.name)
    if request.method == 'POST':
        form = SocietyprofileForm(request.POST, instance=society_profile)
        if form.is_valid():
            form.save()
    else:
        form = SocietyprofileForm(instance=society_profile)
    return render(request, 'society/soc_profile.html', {'socform': form})



User = get_user_model()

def building_list_view(request, id):
    society = None
    buildings = []

    if request.user.is_superuser:
        society = get_object_or_404(Society, id=id)
    else:
        try:
            user = User.objects.get(id=request.user.id)
            society = user.society_name 
        except User.DoesNotExist:
            return render(request, 'building/building_list.html', {'message': 'User not found.'})
        except Exception as e:
            return render(request, 'building/building_list.html', {'message': str(e)})
    
    if society:
        buildings = Building.objects.filter(society__society_name=society)
    
    context = {
        'buildings': buildings,
        'society': society,
    }
    
    return render(request, 'building/building_list.html', context)



User = get_user_model()

def add_building_view(request, id):
    if request.user.is_superuser:
        society = get_object_or_404(Society, id=id)
    else:
        society = get_object_or_404(Society, name=request.user.society.name)

    BuildingFormSet = formset_factory(BuildingForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = BuildingFormSet(request.POST)
        if formset.is_valid():
            try:
                instances = []
                for form in formset:
                    if form.cleaned_data:
                        building = form.save(commit=False)
                        building.society = society
                        building.user = request.user  
                        building.created_by = request.user  
                        building.updated_by = request.user  
                        instances.append(building)
                                 
                        
                Building.objects.bulk_create(instances)
            
                return redirect('building_list', id=society.id)
            except Exception as e:
                error_message = str(e)
        else:
            error_message = 'Formset is not valid. Please check the entered data.'
            return render(request, 'building/add_building.html', {'formset': formset, 'society': society.name, 'error_message': error_message})
    else:
        formset = BuildingFormSet()

    return render(request, 'building/add_building.html', {'formset': formset, 'society': society.name})


def edit_building(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('building_list', id=building.society.id)
    else:
        form = BuildingForm(instance=building)
    
    return render(request, 'building/edit_building.html', {'form': form, 'building': building})


def delete_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.user.is_superuser:
        id = building.id
    else:
        id = request.user.id
    if request.method == 'POST':
        building.delete()
        
        return redirect('building_list', id=id)
    
    return HttpResponseNotAllowed(['POST'])


@login_required
def edit_Societyprofile(request, Societyprofile_id):
    Societyprofile = get_object_or_404(Societyprofile, pk=Societyprofile_id)
    
    if request.method == 'POST':
        print("POST data:", request.POST)  # Log POST data for debugging
        form = SocietyprofileForm(request.POST, instance=Societyprofile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('Societyprofile_list')
            except Exception as e:
                print("An error occurred while saving the form.")
                print(e)
                messages.error(request, "An error occurred while updating the profile.")
        else:
            print("Form is not valid.")
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
                    
            messages.error(request, "There were errors in the form. Please correct them and try again.")
    else:
        form = SocietyprofileForm(instance=Societyprofile)
    
    return render(request, 'society/edit_soc_pro.html', {'form': form})





class BuildingDetailView(DetailView):
    model = Building
    template_name = 'c_build.html'
    context_object_name = 'building'
  
# def floor_data_view(request, building_id):
#     building = get_object_or_404(Building, id=building_id)
#     society_name = building.society.society_name
#     print(f"{building.society}")
#     residents = User.objects.filter(society_sub=society_name, role='resident')

#     if request.method == 'POST':
#         form = UnitForm(request.POST)
#         if form.is_valid():
#             unit = form.save(commit=False)
#             unit.building = building
#             unit.save()
#             return redirect('floor_data', building_id=building.id)
#     else:
#         form = UnitForm()

#     context = {
#         'building': building,
#         'residents': residents,
#         'form': form,
#         'society_name': society_name,
#     }

#     return render(request, 'building/floor_data.html', context)
# # 

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def soc_profile_api(request, id=None):
    society = None

    if request.user.is_superuser:
        society = get_object_or_404(Society, id=id)
    elif request.user.is_admin:
        
        user = get_object_or_404(User, id=request.user.pk)
        print(user.name.pk)

        society = get_object_or_404(Society, name=user.name.name)
    else:
        return Response({"detail": "You don't have permission to access this page."}, status=status.HTTP_403_FORBIDDEN)

    Societyprofile, created = Societyprofile.objects.get_or_create(name=society)

    if request.method == 'POST':
        serializer = SocietyProfileSerializer(Societyprofile, data=request.data)
        if serializer.is_valid():
            serializer.save(name=society)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SocietyProfileSerializer(Societyprofile)
    return Response(serializer.data)