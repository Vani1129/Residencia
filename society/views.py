from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from user.models import Society
from .forms import SocietyProfileForm
from .models import Society_profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse


def home(request):
   return HttpResponse("Welcome to the Society Home Page")


def create_society_profile(request, society_id):
    society_profiles = get_object_or_404(Society, id=society_id)
    society = Society.objects.get(id=society_id)
    if request.method == 'POST':
        form = SocietyProfileForm(request.POST)
        if form.is_valid():
            society_profile = form.save(commit=False)
            society_profile.society_name = society
            society_profile.created_by = request.user
            society_profile.updated_by = request.user
            society_profile.save()
            return redirect(create_society_profile)  # Replace 'success_url' with the appropriate URL name
    else:
        form = SocietyProfileForm()
    return render(request, 'society/create_society_profile.html', {'form': form})
    
@login_required
def society_profile_list(request, society_id=None):
    if request.user.is_superuser and society_id is not None:
        society_profiles = Society_profile.objects.filter(society_name__id=society_id)
    else:
        user = request.user
        print(f"{user.society_name=}")
        society_profiles = Society_profile.objects.filter(society_name__society_name=user.society_name)
        
    context = {
        'society_profiles': society_profiles
    }
    return render(request, 'society/society_profile.html', context)

@login_required
def add_society_profile(request):
    if request.method == 'POST':
        form = SocietyProfileForm(request.POST)
        if form.is_valid():
            society_profile = form.save(commit=False)
            society_profile.created_by = request.user
            society_profile.updated_by = request.user
            society_profile.save()
            messages.success(request, 'Society profile added successfully.')
            return redirect('society_profile_list')
    else:
        form = SocietyProfileForm()
    context = {
        'form': form
    }
    return render(request, 'society/create_society_profile.html', context)

@login_required
def edit_society_profile(request, pk):
    society_profile = get_object_or_404(Society_profile, pk=pk)
    if request.method == 'POST':
        form = SocietyProfileForm(request.POST, instance=society_profile)
        if form.is_valid():
            society_profile = form.save(commit=False)
            society_profile.updated_by = request.user
            society_profile.save()
            messages.success(request, 'Society profile updated successfully.')
            return redirect('society_profile_list')
    else:
        form = SocietyProfileForm(instance=society_profile)
    context = {
        'form': form
    }
    return render(request, 'edit_society_profile.html', context)

@login_required
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

@require_http_methods(["DELETE"])
def delete_society_profile(request, society_profile_id):
    try:
        society_profile = Society_profile.objects.get(pk=society_profile_id)
        society_profile.delete()
        return JsonResponse({'message': 'Society profile deleted successfully.'}, status=200)
    except Society_profile.DoesNotExist:
        return JsonResponse({'error': 'Society profile not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# def edit_society_profile(request, society_profile_id):
#     society_profile = get_object_or_404(Society_profile, pk=society_profile_id)
    
#     if request.method == 'POST':
#         form = SocietyProfileForm(request.POST, instance=society_profile)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('society_profile_list'))  # Redirect to the list page after saving
#     else:
#         form = SocietyProfileForm(instance=society_profile)
    
#     return render(request, 'society/edit_society_profile.html', {'form': form})

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
    
    return render(request, 'society/edit_society_profile.html', {'form': form})
