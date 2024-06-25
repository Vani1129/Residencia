# import json
# from django.http import JsonResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from django.contrib.auth import authenticate,login
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.db import IntegrityError
# from .forms import UserForm, OTPForm, MemberForm, SocietyForm, SubadminForm
# from .utils import generate_otp
# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth import get_user_model
# from django.contrib.auth import logout as auth_logout
# from .models import Society, UserDetails, User
# from django.views.decorators.http import require_http_methods
# from django.shortcuts import get_object_or_404
# from .forms import UserEditForm
# from society.models import Society_profile
# from user.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .forms import UserForm, OTPForm, MemberForm, SocietyForm, SubadminForm, UserEditForm,FamilyMemberForm
from .utils import generate_otp
from .models import Society, UserDetails, Member, FamilyMember
from .serializers import UserLoginSerializer,UserSerializer, FamilyMemberSerializer
from django.contrib.auth import get_user_model
from society.models import Society_profile
from django.contrib.auth.decorators import login_required
from .forms import OTPForm





from django.shortcuts import render, redirect
from .forms import MemberForm, FamilyMemberForm
from society.models import  Building


def resident_list(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    members = Member.objects.filter(building=building)

    context = {
        'building': building,
        'members': members,
    }
    return render(request, 'users/resident_list.html', context)


def add_resident(request, society_id, building_id):
    society = get_object_or_404(Society, id=society_id)
    building = get_object_or_404(Building, id=building_id)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        family_form = FamilyMemberForm(request.POST)
        if form.is_valid() and family_form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')
            flat_type = form.cleaned_data.get('flat_type')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            member_type = form.cleaned_data.get('member_type')

            user_exist_by_phone = User.objects.filter(phone_number=phone).first()
            user_exist_by_email = User.objects.filter(email=email).first()

            if not user_exist_by_phone and not user_exist_by_email:
                user = User.objects.create(
                    full_name=name,
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
                        family_instance = family_form.save(commit=False)
                        family_instance.member = member
                        family_instance.save()

                return redirect('floor_data', building_id=building.id)
            else:
                if user_exist_by_phone:
                    form.add_error('phone_number', "User with this phone number already exists.")
                if user_exist_by_email:
                    form.add_error('email', "User with this email already exists.")
    else:
        form = MemberForm(initial={'society_name_display': society.society_name})
        family_form = FamilyMemberForm()

    context = {
        'form': form,
        'family_form': family_form,
    }
    return render(request, 'building/add_resident.html', context)



def home(request):
    return HttpResponse("Welcome to the Society Home Page")

def register(request, society_id):
    society = get_object_or_404(Society, id=society_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
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
                        full_name=full_name,
                        phone_number=phone_number,
                        email=email,
                        password=password,
                        society_name=society,  # Use the Society instance
                        is_admin=True,
                        image=image,
                    )
                    messages.success(request, 'Registration successful. You can now login.')
                    return redirect('society_id_admin_dashboard', society_id=society.id)
                except IntegrityError as e:
                    messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Invalid form data. Please check the provided information.')
    else:
        society_types = society.type.values_list('name', flat=True)
        form = UserForm(initial={'society_name_display': society.society_name, 'society_type_display': ", ".join(society_types)})

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

# def admin_dashboard(request):
#     return render(request, 'dashboard.html')
UserModel = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request,society_id):
    society = Society.objects.get(id=society_id)
    users = UserModel.objects.filter(society_name=society.society_name)
    # SubadminForm = UserDetails.objects.filter(role='Sub Admin',)
    return render(request, 'registration/admin_dashboard.html', {'users': users})

def society_id_subadmin_list(request, society_id):
    subadmins = UserDetails.objects.filter(society_sub=society_id, role='committee_member')
    return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins, 'society_id': society_id})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login, get_user_model
from .forms import OTPForm

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
        print(f"{form.errors=}")
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            phone_number = form.cleaned_data['phone_number']
            stored_otp = request.session.get('otp')

              # Debugging prints
            print(f"Stored OTP: {stored_otp}")
            print(f"Stored Phone Number: {phone_number}")

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
            print(form.errors)
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = OTPForm(initial={'phone_number': request.session.get('phone_number')})


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
            print(form.cleaned_data)
            types = form.cleaned_data["type"]
            print(f"{form.cleaned_data.get("is_active")=}")
            society = Society.objects.create(
                society_name=form.cleaned_data["society_name"],
                is_active=form.cleaned_data.get("is_active")  # Use get() with a default value
            )
            
            for type_obj in types:
                society.type.add(type_obj)
            
            society.save()
            society_profile = Society_profile.objects.create(
                society_name=society
            )
            society_profile.save()
            print(f"{society_profile=}")
            
            return redirect('show_societies')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = SocietyForm()
    return render(request, 'registration/add_society.html', {'form': form})


def show_societies(request):
    societies = Society.objects.all()
    context = {'societies': societies}
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

    return render(request, 'registration/edit_society.html', {'form': form, 'society': society})



User = get_user_model()

def subadmin_list(request):
    subadmins = UserDetails.objects.filter(society_sub__id=request.user.userdetails.society_sub.id)
    return render(request, 'subadmin_list.html', {'subadmins': subadmins})

def society_id_subadmin_list(request, society_id=None):
   
    subadmins = UserDetails.objects.filter(society_sub__id=society_id)
    return render(request, 'subadmin_list.html', {'subadmins': subadmins, 'society_id': society_id})



def society_id_add_subadmin(request, society_id):
    if request.method == 'POST':
        form = SubadminForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone_no')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')
            # flat_type = form.cleaned_data.get('flat_type')

            user_exist_by_phone = User.objects.filter(phone_number=phone).first()
            user_exist_by_email = User.objects.filter(email=email).first()

            if not user_exist_by_phone and not user_exist_by_email:
                user = User.objects.create_user(
                    full_name=name,
                    phone_number=phone,
                    email=email,
                    is_admin=False
                )
                society = Society.objects.filter(id=society_id).first()
                user_details = UserDetails.objects.create(
                    user=user,
                    role='committee_member',  # Assuming 'committee_member' is the role for subadmins
                    flat_number=flat_number,
                    # flat_type=flat_type,
                    society_sub=society,
                )
                return redirect('society_id_subadmin_list', society_id=society_id)
            else:
                if user_exist_by_phone:
                    form.add_error('phone_no', "User with this phone number already exists.")
                if user_exist_by_email:
                    form.add_error('email', "User with this email already exists.")
        else:
            print(form.errors)
    else:
        form = SubadminForm()

    return render(request, 'registration/add_subadmin.html', {'form': form, 'society_id': society_id})

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
                    full_name=name,
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
                return redirect('society_id_add_subadmin',society_id=society.id)
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

def society_id_subadmin_list(request, society_id):
    subadmins = UserDetails.objects.filter(society_sub=society_id)
    return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins})


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
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information updated successfully.')
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
    else:
        form = UserEditForm(instance=user)
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

def get_society_details(request, society_id):
    society = get_object_or_404(Society, id=society_id)
    data = {
        'id': society.id,
        'society_name': society.society_name,
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
    
@require_http_methods(["DELETE"])
def delete_society(request, society_id):
    try:
        society = Society.objects.get(pk=society_id)
        # society = society.user
        
        society.delete()
        return JsonResponse({'message': 'Society deleted successfully'}, status=200)
    except Society.DoesNotExist:
        return JsonResponse({'message': 'Society not found'}, status=404)
    
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    


def society_details(request, society_id):
    society = get_object_or_404(Society, pk=society_id)
    context = {
        'society': society
    }
    return render(request, 'registration/society_details.html', {'society': society})

def society_id_subadmin_list(request,society_id):
    subadmins = UserDetails.objects.filter(society_sub=society_id)
    return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins})

@user_passes_test(lambda u: u.is_superuser)
def society_id_admin_dashboard(request,society_id):
    society = Society.objects.get(id=society_id)
    users = UserModel.objects.filter(society_name=society.society_name)
    # SubadminForm = UserDetails.objects.filter(role='Sub Admin',)
    return render(request, 'registration/admin_dashboard.html', {'users': users})





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
            elif user.is_staff:
                user_role = "Admin"
            elif user_details and user_details.role == 'committee_member':
                user_role = "Subadmin"
            else:
                user_role = "Member"
            
            # Print role in terminal
            print(f"User logged in: {phone_number} - Role: {user_role}")

            return JsonResponse({
                'success': True, 
                'message': 'OTP verification successful.',
                'user_role': user_role
            })
        except UserModel.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid OTP. Please try again.'}, status=400)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_member_profile(request):
    """
    API endpoint to retrieve member details after OTP verification.
    """
    try:
        user = request.user
        member = Member.objects.get(user=user)

        # Serialize member details
        member_serializer = UserSerializer(member)
        member_data = member_serializer.data

        # Serialize family members associated with this member
        family_members = FamilyMember.objects.filter(member=member)
        family_serializer = FamilyMemberSerializer(family_members, many=True)
        family_data = family_serializer.data

        # Constructing response data
        response_data = {
            'member': member_data,
            'family_members': family_data
        }

        return JsonResponse(response_data)

    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member details not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def member_list(request):
#     if request.method == 'GET':
#         members = Member.objects.filter(user=request.user)
#         serializer = MemberSerializer(members, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = MemberSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def member_detail(request, pk):
#     member = get_object_or_404(Member, pk=pk, user=request.user)

#     if request.method == 'GET':
#         serializer = MemberSerializer(member)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = MemberSerializer(member, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         member.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def family_member_list(request):
#     if request.method == 'GET':
#         family_members = FamilyMember.objects.filter(member__user=request.user)
#         serializer = FamilyMemberSerializer(family_members, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = FamilyMemberSerializer(data=request.data)
#         if serializer.is_valid():
#             member = get_object_or_404(Member, id=request.data.get('member'), user=request.user)
#             serializer.save(member=member)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def family_member_detail(request, pk):
#     family_member = get_object_or_404(FamilyMember, pk=pk, member__user=request.user)

#     if request.method == 'GET':
#         serializer = FamilyMemberSerializer(family_member)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = FamilyMemberSerializer(family_member, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         family_member.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)