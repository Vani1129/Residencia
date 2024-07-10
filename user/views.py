from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Q
from django.http import HttpResponseForbidden

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.utils import timezone
from society.models import Societyprofile 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .forms import (
    UserForm, OTPForm, MemberForm, SocietyForm, SubadminForm, 
    UserEditForm, FamilyMemberForm
)
from .models import (
    Society, UserDetails, Member, FamilyMember, Type
)
from .serializers import (
    UserLoginSerializer, MemberProfileSerializer, 
    MemberCreateUpdateSerializer
)
from .utils import generate_otp
from society.models import Societyprofile, Building


def resident_list(request, id, building_id):
    society = get_object_or_404(Society, id=id)
    building = get_object_or_404(Building, id=building_id)
    members = Member.objects.filter(building=building)

    context = {
        'society': society,
        'building': building,
        'members': members,
    }
    return render(request, 'building/floor_data.html', context)



from django.db import IntegrityError

def add_resident(request, id, building_id):
    society = None
    building = None
        
    if request.user.is_superuser:
        society = get_object_or_404(Society, id=id)
        building = get_object_or_404(Building, id=building_id)
    else:
        usr_id = id
        user = User.objects.get(id=usr_id)
        
        society = user.name
        building = get_object_or_404(Building, id=building_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        family_form = FamilyMemberForm(request.POST)
        
        if form.is_valid() and family_form.is_valid():
            name = form.cleaned_data.get('fullname')
            phone = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')
            flat_type = form.cleaned_data.get('flat_type')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            member_type = form.cleaned_data.get('member_type')
            
            user_exist_by_phone = User.objects.filter(phone_number=phone).exists()
            user_exist_by_email = User.objects.filter(email=email).exists()
        
            if user_exist_by_phone:
                form.add_error('phone_number', "User with this phone number already exists.")
            if user_exist_by_email:
                form.add_error('email', "User with this email already exists.")
            
            if not user_exist_by_phone and not user_exist_by_email:
                try:
                    user = User.objects.create(
                        fullname=name,
                        phone_number=phone,
                        email=email,
                        is_admin=False
                    )
                    
                    member = Member.objects.create(
                        society=society,
                        user=user,
                        building=building,
                        flat_number=flat_number,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        country=country,
                        member_type=member_type
                    )
                    
                    number_of_members = form.cleaned_data.get('number_of_members', 1)
                
                    if number_of_members is not None:
                        for _ in range(number_of_members):
                            try:
                                user_fm = User.objects.create(
                                    fullname=family_form.cleaned_data.get('family_fullname'),
                                    phone_number=family_form.cleaned_data.get('family_phone_number'),                           
                                    is_admin=False
                                )
                                FamilyMember.objects.create(
                                    user=user_fm,
                                    member=member,
                                    fullname=family_form.cleaned_data.get('family_fullname'),
                                    date_of_birth=family_form.cleaned_data.get('family_date_of_birth'),
                                    gender=family_form.cleaned_data.get('family_gender'),
                                    phone_number=family_form.cleaned_data.get('family_phone_number'),
                                    family_relation=family_form.cleaned_data.get('family_relation')
                                )
                            except IntegrityError:
                                # form.add_error('family_phone_number', f"Family member with phone number {family_form.cleaned_data.get('family_phone_number')} already exists.")
                                break
                    
                    if not form.errors:
                        return redirect('floor_data', building_id=building.id, id=society.id)
                
                except IntegrityError:
                    form.add_error('phone_number', "User with this phone number already exists.")
    else:
        form = MemberForm(initial={'name_display': society.name, 'building_display': building.name})
        family_form = FamilyMemberForm()
    
    context = {
        'form': form,
        'family_form': family_form,
        'id': id,
    }
    
    return render(request, 'building/add_resident.html', context)

def edit_resident(request, member_id, id, building_id):
    member = get_object_or_404(Member, id=member_id)
    society = get_object_or_404(Society, id=id)
    building = get_object_or_404(Building, id=building_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        family_member = member.family_members.first()
        family_form = FamilyMemberForm(request.POST, instance=family_member)

        if form.is_valid() and family_form.is_valid():
            form.save()
            family_form.save()
            return redirect('floor_data', building_id=building.id, id=society.id)
    else:
        form = MemberForm(instance=member, initial={'name_display': society.name, 'building_display': building.name})
        family_member = member.family_members.first()
        family_form = FamilyMemberForm(instance=family_member)

    context = {
        'resform': form,
        'resfamily_form': family_form,
        'id': id,
        'building_id': building_id,
    }
    return render(request, 'building/edit_resident.html', context)


def delete_resident(request, resident_id):
    print("Request method:", request.method)
    if request.method == 'DELETE':
        try:
            resident = get_object_or_404(Member, id=resident_id)
            user_id = resident.user.id
            resident.delete()
            User.objects.filter(id=user_id).delete()
            return JsonResponse({'message': 'Resident deleted successfully.'}, status=204)
        except Http404:
            return JsonResponse({'error': 'Resident not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed.'}, status=405)


def home(request):
    return HttpResponse("Welcome to the Society Home Page")

def register(request, id):
    society = get_object_or_404(Society, id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            phone_number = form.cleaned_data.get('phone_number')
            image = form.cleaned_data.get('image')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            UserModel = get_user_model()

            if UserModel.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email address.')
            elif UserModel.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Phone number already exists. Please use a different phone number.')
            else:
                try:
                    user = UserModel.objects.create_user(
                        fullname=fullname,
                        phone_number=phone_number,
                        email=email,
                        password=password,
                        society=society,
                        # name=society.name,  
                        is_admin=True,
                        image=image,
                    )
                    messages.success(request, 'Registration successful. You can now login.')
                    return redirect('id_admin_dashboard', id=society.id)
                except IntegrityError as e:
                    messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Invalid form data. Please check the provided information.')
    else:
        society_types = society.type.values_list('name', flat=True)
        form = UserForm(initial={'name_display': society.name, 'society_type_display': ", ".join(society_types)})

    return render(request, 'registration/register.html', {'form': form, 'society': society})

def login_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier')
            otp = form.cleaned_data.get('otp')
            stored_otp = request.session.get('otp')
            if stored_otp and stored_otp == otp:
                UserModel = get_user_model()
                SubAdminModel = UserDetails()  # Import your SubAdmin model

                try:
                    user = UserModel.objects.get(email=identifier)
                except UserModel.DoesNotExist:
                    try:
                        user = UserModel.objects.get(phone_number=identifier)
                    except UserModel.DoesNotExist:
                        try:
                            subadmin = SubAdminModel.objects.get(phone_number=identifier)  # Check if the identifier is a subadmin phone number
                            user = subadmin.user  # Assuming you have a ForeignKey or OneToOneField from SubAdmin to User
                        except SubAdminModel.DoesNotExist:
                            user = None

                if user:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    messages.success(request, 'OTP verification successful.')
                    return redirect('home')
                else:
                    if len(identifier) == 10 and identifier.isdigit():
                        messages.error(request, 'This phone number is not registered. Please check your number.')
                    else:
                        messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        else:
            messages.error(request, 'Invalid form data. Please check the provided information.')
    else:
        form = OTPForm()
    return render(request, 'registration/login.html', {'form': form})



# def id_subadmin_list(request, id):
#     subadmins = UserDetails.objects.filter(society_sub=id, role='committee_member')
#     return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins, 'id': id})


def send_otp_view(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        identifier = request.POST.get('phone_number')
        UserModel = get_user_model()

        if identifier and len(identifier) == 10 and identifier.isdigit():
            try:
                user = UserModel.objects.get(phone_number=identifier)
            except UserModel.DoesNotExist:
                user = None

            if user is not None:
                otp = '999000'  # Replace with actual OTP generation logic
                request.session['otp'] = otp
                request.session['phone_number'] = identifier
                # Debugging statements
                print(f"Stored OTP: {otp}")
                print(f"Stored Phone Number: {identifier}")
                print(f"Session Data: {request.session.items()}")

                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
                else:
                    messages.success(request, 'OTP sent successfully.')
                    return redirect(reverse('otp_verify') + f"?phone_number={user.phone_number}")
            else:
                error_message = 'This phone number is not registered. Please check your number.'
                if is_ajax:
                    return JsonResponse({'success': False, 'message': error_message})
                else:
                    messages.error(request, error_message)
                    return render(request, 'registration/login.html')
        else:
            error_message = 'Invalid phone number format. Please enter a valid 10-digit phone number.'
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message})
            else:
                messages.error(request, error_message)
                return render(request, 'registration/login.html')
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def otp_page(request):
    return render(request, 'registration/otp_verify.html')



def otp_verify(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            phone_number = form.cleaned_data['phone_number']
            stored_otp = request.session.get('otp')

            if otp_entered == stored_otp and phone_number:
                UserModel = get_user_model()
                try:
                    user = UserModel.objects.get(phone_number=phone_number)
                    login(request, user)
                    messages.success(request, 'OTP verified. You are now logged in.')
                    return redirect('/home/')
                except UserModel.DoesNotExist:
                    messages.error(request, 'User not found. Please try again.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        phone_number = request.session.get('phone_number')
        form = OTPForm(initial={'phone_number': phone_number})

    form.fields['phone_number'].widget.attrs['readonly'] = True

    return render(request, 'registration/otp_verify.html', {'form': form})




def logout_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login
            pass
    return render(request, 'registration/login.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


import logging

logger = logging.getLogger(__name__)


def add_society(request):
    if request.method == 'POST':
        form = SocietyForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            
            society = Society.objects.create(
                name=form.cleaned_data["name"],
                from_date=form.cleaned_data["from_date"],
                to_date=form.cleaned_data.get("to_date"),
                interval=form.cleaned_data.get("interval"),
            )
                        
            for type_obj in form.cleaned_data["type"]:
                society.type.add(type_obj)
            
            society.save()
            
            society_profile = Societyprofile.objects.create(
               society=society,  
                name=society.name
            )
            print("Society profile created:", society_profile.__dict__) 
            
            return redirect('show_societies')
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        form = SocietyForm()
    return render(request, 'registration/add_society.html', {'form': form})


def show_societies(request):
    societies = Society.objects.all()
    context = {'societies': societies}
    for society in societies:
        print(f"Society: {society.name}, Interval: {society.interval}")
    return render(request, 'registration/show_societies.html', context)  # Make sure this matches your actual template path


def edit_society(request, id):
    society = get_object_or_404(Society, id=id)
    if request.method == 'POST':
        form = SocietyForm(request.POST, instance=society)
        if form.is_valid():
            form.save()
            messages.success(request, 'Society updated successfully.')
            return redirect('show_societies')
    else:
        form = SocietyForm(instance=society)

    return render(request, 'registration/edit_society.html', {'socform': form, 'society': society})



User = get_user_model()

def subadmin_list(request, id):
    pass
    # if request.user.is_superuser:
    #     subadmins = UserDetails.objects.filter(society_sub__id=id)
    # elif request.user.is_admin:
    #     usr_id = id
    #     user = User.objects.get(id=usr_id)
    #     print(f"{user.name=}")
        
    #     subadmins = UserDetails.objects.filter(society_sub__name=user.name)

    # # subadmins = UserDetails.objects.filter(society_sub__id=request.user.userdetails.society_sub.id)
    # return render(request, 'subadmin_list.html', {'subadmins': subadmins})

def id_subadmin_list(request, id=None):
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

    # print(f"{request.user=}")
    
    # if request.user.is_superuser:
    #     subadmins = UserDetails.objects.filter(society_sub__id=id)
    # else:
    #     user = get_object_or_404(User, id=id)
    subadmins = UserDetails.objects.filter(id=society.id)
        
    return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins, 'id': id})


def id_add_subadmin(request, id):
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

 
    # subadmins = UserDetails.objects.filter(id=society.id)
    if request.method == 'POST':
        form = SubadminForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone_no')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')

            user_exist_by_phone = User.objects.filter(phone_number=phone).first()
            user_exist_by_email = User.objects.filter(email=email).first()

            if not user_exist_by_phone and not user_exist_by_email:
                society = None
                if request.user.is_superuser:
                    society = Society.objects.filter(id=id).first()
                else:
                    use = User.objects.get(id=id)
                    society = Society.objects.filter(id=use.society.id).first()
                
                user = User.objects.create_user(
                    fullname=name,
                    phone_number=phone,
                    email=email,
                    is_admin=False,
                    society=society  
                )

                user_details = UserDetails.objects.create(
                    user=user,
                    role='committee_member',
                    flat_number=flat_number,
                    society_sub=society,
                )
                return redirect('id_subadmin_list', id=id)
            else:
                if user_exist_by_phone:
                    form.add_error('phone_no', "User with this phone number already exists.")
                if user_exist_by_email:
                    form.add_error('email', "User with this email already exists.")
        else:
            print(form.errors)
    else:
        form = SubadminForm()

    return render(request, 'registration/add_subadmin.html', {'form': form, 'id': id})

def add_subadmin(request):
    print(f"{SubadminForm=}")
    if request.method == 'POST':
        form = SubadminForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone_no')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')
            flat_type = form.cleaned_data.get('flat_type')

            user_exist_by_phone = User.objects.filter(phone_number=phone).first()
            user_exist_by_email = User.objects.filter(email=email).first()

            if not user_exist_by_phone and not user_exist_by_email:
                user = User.objects.create_user(
                    fullname=name,
                    phone_number=phone,
                    email=email,
                    is_admin=False
                )
                print(f"{request.user.userdetails=}")
                userdetail = UserDetails.objects.filter(user=request.user)
                print(f"{userdetail=}")
                
                society = Society.objects.filter(id=request.user.userdetails.society_sub.id).first()
                user_details = UserDetails.objects.create(
                    user=user,
                    role='committee_member',  # Assuming 'committee_member' is the role for subadmins
                    flat_number=flat_number,
                    flat_type=flat_type,
                    society_sub=society,
                )
                return redirect('id_add_subadmin',id=society.id)
            else:
                if user_exist_by_phone:
                    form.add_error('phone_no', "User with this phone number already exists.")
                if user_exist_by_email:
                    form.add_error('email', "User with this email already exists.")
        else:
            print(form.errors)
    else:
        form = SubadminForm()

    return render(request, 'registration/add_subadmin.html', {'form': form})


@csrf_exempt
def delete_subadmin(request, subadmin_id):
    if request.method == 'DELETE':
        subadmin = get_object_or_404(UserDetails, id=subadmin_id)
        subadmin.delete()
        return JsonResponse({'message': 'Subadmin deleted successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def edit_subadmin(request, pk):
    subadmin = get_object_or_404(UserDetails, pk=pk)
    if request.method == 'POST':
        form = SubadminForm(request.POST, instance=subadmin)
        if form.is_valid():
            form.save()
            return redirect('subadmin_list') 
    else:
        form = SubadminForm(instance=subadmin)
    return render(request, 'registration/edit_subadmin.html', {'form': form, 'subadmin': subadmin})




def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_dashboard', user_id=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'registration/edit_user.html', {'form': form, 'user': user})




def dashboard(request):
    user = request.user
    context = {'user': user}
    print(f"{user.role=}")
    
    print(f"{user.role=}")
    if user.role == 'Super Admin':
        context['is_superadmin'] = True
    elif user.role == 'Admin':
        context['is_admin'] = True
    elif user.role == 'Sub Admin':
        context['is_subadmin'] = True
    
    return render(request, 'dashboard.html', context)

def get_society_details(request, id):
    society = get_object_or_404(Society, id=id)
    data = {
        'id': society.id,
        'name': society.name,
        'type': society.type,
        'is_active': society.is_active,
    }
    return JsonResponse(data)


@require_http_methods(["DELETE"])
def delete_subadmin(request, subadmin_id):

    try:
        subadmin = UserDetails.objects.get(pk=subadmin_id)
        user = subadmin.user
        subadmin.delete()
        user.delete()
        return JsonResponse({'message': 'Subadmin deleted successfully'}, status=200)
    except UserDetails.DoesNotExist:
        return JsonResponse({'message': 'Subadmin not found'}, status=404)
    


@require_http_methods(["POST", "DELETE"])
def delete_society(request, id):
    try:
        society = Society.objects.get(id=id)
        society.delete()
        messages.success(request, 'Society deleted successfully')
    except Society.DoesNotExist:
        messages.error(request, 'Society not found')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('show_societies') 



    
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    



def society_details(request, id):
    society = get_object_or_404(Society, id=id)
    # Societyprofile = Societyprofile.objects.filter(name=society).first()

    # print(Societyprofile.address) 
    
    return render(request, 'registration/society_details.html', {
        'society': society,
        # 'Societyprofile': Societyprofile,
    })


UserModel = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request,id):
    society = Society.objects.get(id=id)
    users = User.objects.filter(name=society.name,is_admin=True)
    return render(request, 'registration/admin_dashboard.html', {'users': users, 'society': society})

@user_passes_test(lambda u: u.is_superuser)
def id_admin_dashboard(request,id):
    society = Society.objects.get(id=id)
    users = User.objects.filter(is_admin=True).filter(~Q(is_staff=True))
    return render(request, 'registration/admin_dashboard.html', {'users': users, 'society':society})


@login_required
def member_list(request):
    members = Member.objects.filter(user=request.user)
    return render(request, 'member_list.html', {'members': members})

@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk, user=request.user)
    return render(request, 'member_detail.html', {'member': member})

@login_required
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, 'Member created successfully.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'member_form.html', {'form': form})

@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'member_form.html', {'form': form, 'member': member})

@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk, user=request.user)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted successfully.')
        return redirect('member_list')
    return render(request, 'member_confirm_delete.html', {'member': member})

@login_required
def family_member_list(request):
    family_members = FamilyMember.objects.filter(member__user=request.user)
    return render(request, 'family_member_list.html', {'family_members': family_members})

@login_required
def family_member_detail(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk, member__user=request.user)
    return render(request, 'family_member_detail.html', {'family_member': family_member})

@login_required
def family_member_create(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            family_member = form.save(commit=False)
            family_member.member = get_object_or_404(Member, pk=form.cleaned_data['member'].pk, user=request.user)
            family_member.save()
            messages.success(request, 'Family member created successfully.')
            return redirect('family_member_detail', pk=family_member.pk)
    else:
        form = FamilyMemberForm()
    return render(request, 'family_member_form.html', {'form': form})

@login_required
def family_member_update(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk, member__user=request.user)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, instance=family_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family member updated successfully.')
            return redirect('family_member_detail', pk=family_member.pk)
    else:
        form = FamilyMemberForm(instance=family_member)
    return render(request, 'family_member_form.html', {'form': form, 'family_member': family_member})

@login_required
def family_member_delete(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk, member__user=request.user)
    if request.method == 'POST':
        family_member.delete()
        messages.success(request, 'Family member deleted successfully.')
        return redirect('family_member_list')
    return render(request, 'family_member_confirm_delete.html', {'family_member': family_member})




#api

UserModel = get_user_model()

@swagger_auto_schema(method='post', request_body=UserLoginSerializer, responses={200: 'OTP sent successfully.', 400: 'Invalid identifier format.'})
@api_view(['POST'])
@permission_classes([])
def api_send_otp(request):
    """
    Send OTP to the user's phone number.
    """
    identifier = request.data.get('phone_number')
    if len(identifier) == 10 and identifier.isdigit():
        try:
            user = UserModel.objects.get(phone_number=identifier)
            otp = '999000'
            request.session['otp'] = otp
            print(f"Generated OTP: {otp}")  # Debugging line, should be removed in production
            
            return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
        except UserModel.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'This phone number is not registered.'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid identifier format.'}, status=400)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer, responses={200: 'OTP verification successful.', 400: 'Invalid OTP. Please try again.', 404: 'User not found.'})
@api_view(['POST'])
@permission_classes([])
@csrf_exempt
def api_verify_otp(request):
    """
    Verify the OTP sent to the user's phone number and log in the user.
    """
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    stored_otp = request.session.get('otp', '999000')

    if stored_otp == otp:
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            user_details = user.userdetails.first()

            # Determine user role
            if user.is_superuser:
                user_role = "Super Admin"
            elif user.is_admin:
                user_role = "Admin"
            elif user_details and user_details.role == 'committee_member':
                user_role = "Subadmin"
            else:
                user_role = "Member"
            
            # Print role in terminal
            print(f"User logged in: {phone_number} - Role: {user_role}")
            
            token, created   = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'success': True, 
                'message': 'OTP verification successful.',
                'user_role': user_role,
                'token': token.key,
                
            })
        except UserModel.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid OTP. Please try again.'}, status=400)
    

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def api_member_profile(request):
    user = request.user

    if request.method == 'GET':
        try:
            member = Member.objects.get(user=user)
            member_serializer = MemberProfileSerializer(member)
            return Response({'member': member_serializer.data})
        except Member.DoesNotExist:
            return Response({'error': 'Member details not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error retrieving member details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        member_serializer = MemberCreateUpdateSerializer(data=request.data)
        
        if member_serializer.is_valid():
            try:
                member_serializer.save(user=user)
                return Response({'message': 'Member details saved successfully.'})
            except Exception as e:
                return Response({'error': 'Error saving member details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            member = Member.objects.get(user=user)
            member_serializer = MemberCreateUpdateSerializer(member, data=request.data, partial=True)
            
            if member_serializer.is_valid():
                member_serializer.save()
                return Response({'message': 'Member details updated successfully.'})
            else:
                return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Member.DoesNotExist:
            return Response({'error': 'Member details not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error updating member details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
