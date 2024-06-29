from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from user.models import Society

from .models import Society_profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import DetailView
from .models import Society, Building, Unit
from django.http import JsonResponse
from .models import Society_profile, Society
from .forms import SocietyProfileForm, BuildingForm, UnitForm, UnitForm
from .models import Building, Unit, UserDetails
from user.models import User


def home(request):
   return HttpResponse("Welcome to the Society Home Page")



def soc_profile(request, society_id=None):
    print(f"{society_id=}")
    society = None
    society_profile = None

    if request.user.is_superuser:
        society = get_object_or_404(Society, id=society_id)
    elif request.user.is_admin:
        user = get_object_or_404(User, id=society_id)
        society = get_object_or_404(Society, society_name=user.society_name)
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

    society_profile, created = Society_profile.objects.get_or_create(society_name=society)

    if request.method == 'POST':
        form = SocietyProfileForm(request.POST, instance=society_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.society_name = society  # Ensure the society is set
            profile.save()
            return redirect('society_id_soc_profile',society_id=society_id)  # Redirect after successful save
    else:
        initial_data = {
            'society_name_display': society.society_name,
            'society_type_display': ', '.join([str(t) for t in society.type.all()])
        }
        form = SocietyProfileForm(instance=society_profile, initial=initial_data)

    return render(request, 'society/soc_profile.html', {'socform': form})

def society_profile_admin_view(request):
    
       
    society_profile = get_object_or_404(Society_profile, society_name_society_name=request.user.society_name)
    if request.method == 'POST':
        form = SocietyProfileForm(request.POST, instance=society_profile)
        if form.is_valid():
            form.save()
    else:
        form = SocietyProfileForm(instance=society_profile)
    return render(request, 'society/soc_profile.html', {'socform': form})


def building_list_view(request, society_id):
    society = None
    if request.user.is_superuser:
        society = get_object_or_404(Society, id=society_id)
    else:
        user = User.objects.get(id=society_id)
        print(f"{user=}")
        print(f"{user.society_name=}")
        
        society = Society.objects.filter(society_name=user.society_name).first()
        print(f"{society=}")
        
    buildings = Building.objects.filter(society__society_name=society)
    # print(f"{buildings=}")
    return render(request, 'building/building_list.html', {'buildings': buildings, 'society': society})


def add_building_view(request, society_id):
    society = None
    society_profile = None
    if request.user.is_superuser:
        society = get_object_or_404(Society, id=society_id)
        print(f"Looking up Society_profile with society_name={society}")
        society_profile = get_object_or_404(Society_profile, society_name=society)
    else:
        user = User.objects.get(id=request.user.id)
        print(f"{user.society_name=}")
        society_profile = get_object_or_404(Society_profile, society_name__society_name=user.society_name)
        society = society_profile.society_name
    
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.society = society_profile  # Assign the society_profile instance here
            building.save()
            print(f"{society_id=}")
            return redirect('building_list', society_id=society.id if request.user.is_superuser else request.user.id)
            
    else:
        form = BuildingForm(initial={'society_name_display': society.society_name})
    
    return render(request, 'building/add_building.html', {'form': form, 'society': society})

def edit_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('your_building_list_view')  # Replace with your actual view name
    else:
        form = BuildingForm(instance=building)
    return render(request, 'building/edit_building.html', {'form': form})

def delete_building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    if request.method == 'POST':
        building.delete()
        return redirect('your_building_list_view')  # Replace with your actual view name
    return render(request, 'building/delete_building.html', {'building': building})


def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('your_unit_list_view')  # Replace with your actual view name
    else:
        form = UnitForm()
    return render(request, 'building/add_unit.html', {'form': form})

def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('your_unit_list_view')  # Replace with your actual view name
    else:
        form = UnitForm(instance=unit)
    return render(request, 'building/edit_unit.html', {'form': form})

def delete_unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    if request.method == 'POST':
        unit.delete()
        return redirect('your_unit_list_view')  # Replace with your actual view name
    return render(request, 'building/delete_unit.html', {'unit': unit})

def unit_list(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    units = building.unit_set.all()  # Assuming a related name of 'unit_set'
    form = UnitForm()
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.building = building
            unit.save()
            return redirect('unit_list', building_id=building.id)
    return render(request, 'building/unit_list.html', {'building': building, 'units': units, 'form': form})



@login_required
def edit_society_profile(request, society_profile_id):
    society_profile = get_object_or_404(Society_profile, pk=society_profile_id)
    
    if request.method == 'POST':
        print("POST data:", request.POST)  # Log POST data for debugging
        form = SocietyProfileForm(request.POST, instance=society_profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('society_profile_list')
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
        form = SocietyProfileForm(instance=society_profile)
    
    return render(request, 'society/edit_soc_pro.html', {'form': form})



# def delete_society_profile(request, pk):
#     society_profile = get_object_or_404(Society_profile, pk=pk)
#     if request.method == 'POST':
#         society_profile.delete()
#         messages.success(request, 'Society profile deleted successfully.')
#         return redirect('society_profile_list')
#     context = {
#         'society_profile': society_profile
#     }
#     return render(request, 'delete_society_profile.html', context)


    



class BuildingDetailView(DetailView):
    model = Building
    template_name = 'c_build.html'
    context_object_name = 'building'

class UnitDetailView(DetailView):
    model = Unit
    template_name = 'c_unit.html'
    context_object_name = 'unit'
    
    
def floor_data_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    society_name = building.society.society_name
    units = Unit.objects.filter(building=building)
    print(f"{building.society}")
    residents = UserDetails.objects.filter(society_sub=society_name, role='resident')

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.building = building
            unit.save()
            return redirect('floor_data', building_id=building.id)
    else:
        form = UnitForm()

    context = {
        'building': building,
        'units': units,
        'residents': residents,
        'form': form,
        'society_name': society_name,
    }

    return render(request, 'building/floor_data.html', context)


# def floor_data_view(request, building_id):
#     building = get_object_or_404(Building, id=building_id)
    
#     units = Unit.objects.filter(building=building)
#     if request.method == 'POST':
#         form = UnitForm(request.POST)
#         if form.is_valid():
#             unit = form.save(commit=False)
#             unit.building = building
#             unit.save()
#             return redirect('floor_data', building_id=building.id)
#     else:
#         form = UnitForm()
#     return render(request, 'building/floor_data.html', {'building': building, 'units': units, 'form': form})