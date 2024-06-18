import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .forms import UserForm, OTPForm, MemberForm, SocietyForm, SubadminForm
from .utils import generate_otp
from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from django.views.decorators.http import require_POST
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from .models import Society, UserDetails, User
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .forms import UserEditForm




def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully.')
            return redirect('home')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

def home(request):
    return HttpResponse("Welcome to the Society Home Page")

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            phone_number = form.cleaned_data.get('phone_number')
            image = form.cleaned_data.get('image')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            address = form.cleaned_data.get('address')
            society = form.cleaned_data.get('society_name')  # Update to use the Society instance
            # role = form.cleaned_data.get('role')  # Assuming role is a field in your form
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
                        address=address,
                        society_name=society,
                        is_admin=True,# Use the Society instance
                        # role=role,  # Save the role to the user
                        image=image,
                    )
                    society_details = Society.objects.get(society_name=society)
                    messages.success(request, 'Registration successful. You can now login.')
                    return redirect('society_id_admin_dashboard', society_id=society_details.id)
                except IntegrityError as e:
                    messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Invalid form data. Please check the provided information.')
    else:
        form = UserForm()
    
    return render(request, 'registration/register.html', {'form': form})



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

def society_id_subadmin_list(request,society_id):
    subadmins = UserDetails.objects.filter(society_sub=society_id)
    return render(request, 'registration/subadmin_list.html', {'subadmins': subadmins})



def send_otp_view(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        identifier = request.POST.get('identifier')
        UserModel = get_user_model()

        if len(identifier) == 10 and identifier.isdigit():
            try:
                user = UserModel.objects.get(phone_number=identifier)
            except UserModel.DoesNotExist:
                user = None

            if user is not None:
                otp = generate_otp()
                request.session['otp'] = otp
                # Here, you should send the OTP via email/SMS. For example, you can use Django's send_mail function or an SMS API.
                print(f"Generated OTP: {otp}")  # Debugging line, should be removed in production

                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
                else:
                    messages.success(request, 'OTP sent successfully.')
                    return redirect('otp_verify')
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'message': 'This phone number is not registered. Please check your number.'})
                else:
                    messages.error(request, 'This phone number is not registered. Please check your number.')
                    return render(request, 'registration/login.html')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Invalid identifier format. Please enter a valid phone number.'})
            else:
                messages.error(request, 'Invalid identifier format. Please enter a valid phone number.')
                return render(request, 'registration/login.html')
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}) 

def otp_verify(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            stored_otp = request.session.get('otp')
            if stored_otp and stored_otp == otp:
                messages.success(request, 'OTP verification successful.')
                return redirect("login")
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        else:
            messages.error(request, 'Invalid form data. Please check the provided information.')
    else:
        form = OTPForm()
    return render(request, 'registration/otp_verify.html', {'form': form})


# User = get_user_model()

# @require_POST
# def delete_user(request):
#     user_id = request.POST.get('user_id')
#     try:
#         user = User.objects.get(pk=user_id)
#         user.delete()
#         return JsonResponse({'success': True})
#     except User.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    
    
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
            print(form.cleaned_data)  # Print cleaned data for debugging
            form.save()
            return redirect('show_societies')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = SocietyForm()
    return render(request, 'registration/add_society.html', {'form': form})


# def update_society(request, society_id):
#     society = get_object_or_404(Society, id=society_id)

#     if request.method == 'POST':
#         form = SocietyForm(request.POST, request.FILES, instance=society)
#         if form.is_valid():
#             form.save()
#             return redirect('registration/show_societies')
#     else:
#         form = SocietyForm(instance=society)

#     return render(request, 'registration/update_society.html', {'form': form})


def show_societies(request):
    societies = Society.objects.all()
    context = {'societies': societies}
    return render(request, 'registration/show_societies.html', context)  # Make sure this matches your actual template path

# def show_society(request, society_id):
#     society = Society.objects.get(pk=society_id)
#     user_details = UserDetails.objects.get(user=request.user)
#     context = {
#         'society': society,
#         'user_details': user_details,
#         'society_id': society_id,
#     }
#     return render(request, 'registration/show_societies.html', context)

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


def add_subadmin(request):
    if request.method == 'POST':
        form = SubadminForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone_no')
            email = form.cleaned_data.get('email')
            flat_number = form.cleaned_data.get('flat_number')
            flat_type = form.cleaned_data.get('flat_type')

            # Check if a user with the given phone number or email already exists
            user_exist_by_phone = User.objects.filter(phone_number=phone).first()
            user_exist_by_email = User.objects.filter(email=email).first()

            if not user_exist_by_phone and not user_exist_by_email:
                # Create a new user
                user = User.objects.create_user(
                    full_name=name,
                    phone_number=phone,
                    email=email,
                    is_admin=False
                )
                
                # Create a new UserDetails instance and associate it with the user
                user_details = UserDetails.objects.create(
                    user=user,
                    role='committee_member',  # Assuming 'committee_member' is the role for subadmins
                    flat_number=flat_number,
                    flat_type=flat_type,
                )

                # No need to save form as the relevant data is saved through the creation above
                # form.save()

                # Optionally, you can log in the user here if needed
                # login(request, user)

                # Redirect to the subadmin list
                return redirect('subadmin_list')
            else:
                if user_exist_by_phone:
                    form.add_error('phone_no', "User with this phone number already exists.")
                if user_exist_by_email:
                    form.add_error('email', "User with this email already exists.")
        else:
            print(form.errors)  # Print form errors for debugging

    else:
        form = SubadminForm()

    return render(request, 'registration/add_subadmin.html', {'form': form})


def subadmin_list(request):
    subadmins = UserDetails.objects.all()
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
    
# def societies_list(request):
#     societies = Society.objects.all()
#     context = {
#         'societies': societies
#     }
#     return render(request, 'registration/societies_list.html', context)

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

