from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Amenity
from .forms import AmenityForm

class AmenityListView(ListView):
    model = Amenity
    template_name = 'amenity/cms/amenities.html'
    context_object_name = 'amenities'

def add_amenity(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('amenities')
    else:
        form = AmenityForm()
    return render(request, 'amenity/cms/add.html', {'ameform': form})

def edit_amenity(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenities')
    else:
        form = AmenityForm(instance=amenity)
    return render(request, 'amenity/cms/edit.html', {'eform': form})

def delete_amenity(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        amenity.delete()
        return redirect('amenities')
    return render(request, 'amenity/cms/confirm_delete.html', {'amenity': amenity})
