from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .models import Amenity
# from django.contrib.auth.models importUser
from .forms import AmenityForm
from user.models import Society,  User
from django.contrib.auth.decorators import login_required


def amenities(request, id):
    society=None
    if request.user.is_superuser:
        society = get_object_or_404(Society, pk=id)
    elif request.user.is_admin:
        if id == request.user.id:
            society = request.user.society
        else:
            society = get_object_or_404(Society, pk=id)
    # else:
    #     society = request.user.society
    #     if society.id != id:
    #         return HttpResponseForbidden("You don't have permission to access this society's profile.")

    amenities = Amenity.objects.filter(pk=id)
    

    context = {

        'amenities': amenities,
        'society': society,
        'pk': id,
    }

    return render(request, 'amenity/cms/amenities.html', context)


@login_required
def add_amenity(request, id):
    society=None
    if request.user.is_superuser:
        society = get_object_or_404(Society, pk=id)
    else:
        society = request.user.society
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            amenity = form.save(commit=False)
            amenity.society = society  
            amenity.user = request.user
            amenity.save()
            return redirect('amenities', id=society.id if request.user.is_superuser else request.user.id)

    else:
        form = AmenityForm(initial={'name_display': society.name if hasattr(society, 'name') else society})
       
    context = {
        'ameform': form,
        'society': society,
        'id': society.id,
    }
    return render(request, 'amenity/cms/add.html', context)


def edit_amenity(request, pk):
    society=None
    if request.user.is_superuser:
        society = get_object_or_404(Society, pk=id)
    else:
        society = request.user.society
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenities')
    else:
        form = AmenityForm(instance=amenity)

    context = {
        'eform': form,
        'society': society,
        'pk': pk,
    }
    return render(request, 'amenity/cms/edit.html', context)


def delete_amenity(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        amenity.delete()
        return redirect('amenities')
    return render(request, 'amenity/cms/confirm_delete.html', {'amenity': amenity})