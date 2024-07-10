
# views.py
from django.http import JsonResponse,HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommunicationForm
from .models import Communication
from django.contrib import messages
# from django.contrib.auth.models import User
from user.models import Society, User
from django.contrib.auth.decorators import login_required
from .models import Communication
from django.urls import reverse
from .models import Communication
from user.models import Society, User


def main_comm(request, id):
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

    communications = Communication.objects.filter(id=id)

    # if pk is not None:
        # communications = communications.filter(pk=pk)

    context = {
        'communications': communications,
        'society': society,
        # 'pk' :pk,
        'id': id,
    }

    return render(request, 'communication/cms/main_page.html', context)


def create_communication(request, id):
    society=None
    if request.user.is_superuser:
        society = get_object_or_404(Society, pk=id)
    else:
        society = request.user.society
  
    if request.method == 'POST':
        form = CommunicationForm(request.POST, request.FILES)
        if form.is_valid():
            communication = form.save(commit=False)
            communication.society = society
            communication.user = request.user
            communication.save()
            return  redirect('main', id=society.id if request.user.is_superuser else request.user.id)
        
    else:
        form = CommunicationForm()

    return render(request, 'communication/cms/create_communication.html', {'communform': form, 'society': society})

# def create_communication(request, id):
#     society = get_object_or_404(Society, id=id)

#     if request.method == 'POST':
#         form = CommunicationForm(request.POST)
#         if form.is_valid():
#             communication = form.save(commit=False)
#             communication.id = id
#             communication.save()
#             return redirect('main', id=society.id)
#     else:
#         form = CommunicationForm()
#     return render(request, 'communication/cms/create_communication.html', {'communform': form, 'id': id})


def edit_communication(request, pk, id):
    communication = get_object_or_404(Communication, pk=pk)
    society = get_object_or_404(Society, id=id)

    if request.method == 'POST':
        form = CommunicationForm(request.POST, instance=communication)
        if form.is_valid():
            form.save()
            return redirect('main', id=society.id if request.user.is_superuser else request.user.id)
    else:
        form = CommunicationForm(instance=communication)
    context = {
        'commform': form,
        'id': id,
        'society': society,
    }
    return render(request, 'communication/cms/edit_communication.html', context)


def delete_comm(request, pk, id):
    communication = get_object_or_404(Communication, pk=pk)
    society = get_object_or_404(Society, id=id)

    if request.method == 'POST':
        communication.delete()
        return redirect('main_comm', id=society.id if request.user.is_superuser else request.user.id)

    context = {
        'communication': communication,
        'id': id,
        'society': society,
    }
    return render(request, 'communication/cms/delete_communication.html', context)

# def delete_comm(request):
#     if request.method == 'POST':
#         comm_id = request.POST.get('comm_id')
#         id = request.POST.get('id')
#         try:
#             communication = Communication.objects.get(pk=comm_id, id=id)
#             communication.delete()
#             return JsonResponse({'success': True})
#         except Communication.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Announcement not found.'})
#     return JsonResponse({'success': False, 'error': 'Invalid request.'})